import pandas as pd

# Read CSV
df = pd.read_csv(
    r"C:\Users\saumy\OneDrive\Desktop\job courses\New folder\demand forecasting\data\data.csv",
    encoding="cp1252"
)

# Revenue
df["Revenue"] = df["UnitPrice"] * df["Quantity"]

# Save

df.to_csv(
    r"C:\Users\saumy\OneDrive\Desktop\job courses\New folder\demand forecasting\data\data_with_revenue.csv",
    index=False
)

print(df.head())