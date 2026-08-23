import pandas as pd

# Read the cleaned CSV
df = pd.read_csv(
    r"C:\Users\saumy\OneDrive\Desktop\job courses\New folder\demand forecasting\data\1.data_with_revenue.csv",
    encoding="cp1252"
)

# SUMIFS equivalent
summary = (
    df.groupby(
        ["CustomerID", "StockCode"],
        as_index=False,
        dropna=False
    )
    .agg(
        Total_Revenue=("Revenue", "sum"),
        Total_Quantity=("Quantity", "sum")
    )
)

# Calculate Average Unit Price
summary["Average_Unit_Price"] = (
    summary["Total_Revenue"] /
    summary["Total_Quantity"]
)

# Save
summary.to_csv(
    r"C:\Users\saumy\OneDrive\Desktop\job courses\New folder\demand forecasting\data\3.customer_stock_summary.csv",
    index=False
)

print(summary.head(5))
print("Done! Summary table saved.")