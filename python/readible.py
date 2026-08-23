import pandas as pd

# Read CSV
df = pd.read_csv(
    r"C:\Users\saumy\OneDrive\Desktop\job courses\New folder\demand forecasting\data\data.csv",
    encoding="cp1252"
)

# -----------------------------
# Set column data types
# -----------------------------

# Text
df["InvoiceNo"] = df["InvoiceNo"].astype("string")
df["StockCode"] = df["StockCode"].astype("string")
df["Description"] = df["Description"].astype("string")
df["Country"] = df["Country"].astype("string")

# Numbers
df["Quantity"] = pd.to_numeric(df["Quantity"], errors="coerce")
df["UnitPrice"] = pd.to_numeric(df["UnitPrice"], errors="coerce")
df["CustomerID"] = pd.to_numeric(df["CustomerID"], errors="coerce")

# Date & Time
df["InvoiceDate"] = pd.to_datetime(
    df["InvoiceDate"],
    errors="coerce"
)

# Revenue
df["Revenue"] = df["UnitPrice"] * df["Quantity"]

# -----------------------------
# Number formatting
# -----------------------------

# Quantity → whole numbers
df["Quantity"] = df["Quantity"].round(0).astype("Int64")

# UnitPrice → 2 decimal places
df["UnitPrice"] = df["UnitPrice"].round(2)

# CustomerID → whole numbers
df["CustomerID"] = df["CustomerID"].round(0).astype("Int64")

# Revenue → 2 decimal places
df["Revenue"] = df["Revenue"].round(2)

# -----------------------------
# Save
# -----------------------------

df.to_csv(
    r"C:\Users\saumy\OneDrive\Desktop\job courses\New folder\demand forecasting\data\data_with_revenue.csv",
    index=False
)

# Show first 5 rows
print(df.head())

# Show data types
print("\nData types:")
print(df.dtypes)