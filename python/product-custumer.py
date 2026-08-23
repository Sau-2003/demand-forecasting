import pandas as pd

# Read the cleaned CSV
df = pd.read_csv(
    r"C:\Users\saumy\OneDrive\Desktop\job courses\New folder\demand forecasting\data\data_with_revenue.csv",
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

# Round numbers
summary["Total_Revenue"] = summary["Total_Revenue"].round(2)
summary["Average_Unit_Price"] = summary["Average_Unit_Price"].round(2)

# Save
summary.to_csv(
    r"C:\Users\saumy\OneDrive\Desktop\job courses\New folder\demand forecasting\data\customer_stock_summary.csv",
    index=False
)

# Display first 5 rows
print(summary.head(5))

print("Done! Summary table saved.")