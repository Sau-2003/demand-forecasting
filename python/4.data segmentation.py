import pandas as pd

# 1. READ data_with_revenue
df_main = pd.read_csv(
    r"C:\Users\saumy\OneDrive\Desktop\job courses\New folder\demand forecasting\data\1.data_with_revenue.csv",
    encoding="cp1252",
    dtype={"StockCode": str}
)

# StockCode MUST remain text
df_main["StockCode"] = df_main["StockCode"].astype(str)


# 2. READ CUSTOMER SEGMENTATION
df_seg = pd.read_csv(
    r"C:\Users\saumy\OneDrive\Desktop\job courses\New folder\demand forecasting\data\3.customer_segmentation.csv"
)

# Only take CustomerID + Customer_Size
seg_subset = df_seg[
    ["CustomerID", "Customer_Size"]
].copy()


# 3. JOIN BY CustomerID
# Keep ALL rows from data_with_revenue
df_main = df_main.merge(
    seg_subset,
    on="CustomerID",
    how="left"
)


# 4. SORT BY STOCKCODE (ASCENDING) & INVOICE
df_main = (
    df_main
    .sort_values(
        by=["StockCode", "InvoiceNo"],
        ascending=[True, True]
    )
    .reset_index(drop=True)
)


# 5. CUMULATIVE QUANTITY
df_main["Product_Cumulative_Volume"] = (
    df_main
    .groupby("StockCode", sort=False)["Quantity"]
    .cumsum()
)


# 6. TOTAL QUANTITY FOR EACH STOCKCODE
total_quantity = (
    df_main
    .groupby("StockCode")["Quantity"]
    .transform("sum")
)


# 7. VOLUME PERCENTILE
df_main["Product_Volume_Percentile_%"] = (
    df_main["Product_Cumulative_Volume"]
    / total_quantity
    * 100
).round(2)


# 8. CREATE ADJUSTED UNIT PRICE
def calculate_adjusted_price(group):

    group = group.copy()

    # 25% REFERENCE-LARGE CUSTOMER
    large_rows = group[group["Customer_Size"] == "Large"]
    large_25 = large_rows[large_rows["Product_Volume_Percentile_%"] >= 25]

    if not large_25.empty:
        large_price_25 = large_25["UnitPrice"].iloc[0]
    else:
        large_price_25 = group["UnitPrice"].iloc[0]


    # 50% REFERENCE-MEDIUM CUSTOMER
    medium_rows = group[group["Customer_Size"] == "Medium"]
    medium_50 = medium_rows[medium_rows["Product_Volume_Percentile_%"] >= 50]

    if not medium_50.empty:
        medium_price_50 = medium_50["UnitPrice"].iloc[0]
    else:
        medium_price_50 = group["UnitPrice"].iloc[0]


    # 75% REFERENCE-SMALL CUSTOMER
    small_rows = group[group["Customer_Size"] == "Small"]
    small_75 = small_rows[small_rows["Product_Volume_Percentile_%"] >= 75]

    if not small_75.empty:
        small_price_75 = small_75["UnitPrice"].iloc[0]
    else:
        small_price_75 = group["UnitPrice"].iloc[0]


    # CREATE NEW PRICE
    def get_adjusted_price(row):
        percentile = row["Product_Volume_Percentile_%"]
        current_price = row["UnitPrice"]

        if percentile <= 25:
            return max(current_price, large_price_25)
        elif percentile <= 50:
            return max(current_price, medium_price_50)
        elif percentile <= 75:
            return max(current_price, small_price_75)
        else:
            return current_price

    group["Adjusted_UnitPrice"] = (
        group.apply(get_adjusted_price, axis=1)
    )

    return group

df_main = (
    df_main
    .groupby("StockCode", group_keys=False)
    .apply(calculate_adjusted_price)
    .reset_index(drop=True)
)


# 9. NEW REVENUE
df_main["New_Revenue"] = (
    df_main["Adjusted_UnitPrice"] * df_main["Quantity"]
).round(2)


# 10. CALCULATE TOTALS
old_revenue_total = df_main["Revenue"].sum()
new_revenue_total = df_main["New_Revenue"].sum()
profit_difference = new_revenue_total - old_revenue_total


# 11. WRITE TOTALS TO DATAFRAME & SAVE AS CSV

# Create two new columns at the far right of the CSV, filled with blanks
df_main["Total_Old_Revenue"] = ""
df_main["Total_New_Revenue"] = ""
df_main["Profit_Difference"] = ""

# Insert the sums into just the very first row (index 0)
df_main.at[0, "Total_Old_Revenue"] = round(old_revenue_total, 2)
df_main.at[0, "Total_New_Revenue"] = round(new_revenue_total, 2)
df_main.at[0, "Profit_Difference"] = round(profit_difference, 2)

# Save it as a normal CSV (Overwriting your previous file)
df_main.to_csv(
    r"C:\Users\saumy\OneDrive\Desktop\job courses\New folder\demand forecasting\data\5.data_with_segments.csv",
    index=False
)


# 12. DISPLAY RESULTS IN TERMINAL
cols_to_show = [
    "StockCode",
    "Quantity",
    "UnitPrice",
    "Adjusted_UnitPrice",
    "Revenue",
    "New_Revenue",
]

print(df_main[cols_to_show].head(5))
print("\nDone!")