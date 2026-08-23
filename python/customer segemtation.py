import pandas as pd
import numpy as np

# 1. Read the customer-stock summary
df = pd.read_csv(
    r"C:\Users\saumy\OneDrive\Desktop\job courses\New folder\demand forecasting\data\customer_stock_summary.csv",
    encoding="cp1252"
)

# 2. Sum Total Revenue for each unique CustomerID
customer_segmentation = (
    df.groupby("CustomerID", dropna=False)["Total_Revenue"]
    .sum()
    .reset_index()
)
customer_segmentation["Total_Revenue"] = customer_segmentation["Total_Revenue"].round(2)

# 3. Apply the clean custom bins
custom_bins = [-np.inf, 3500, 40000, np.inf]
segment_labels = ["Small", "Medium", "Large"]

customer_segmentation["Customer_Size"] = pd.cut(
    customer_segmentation["Total_Revenue"], 
    bins=custom_bins, 
    labels=segment_labels
)

# 4. Save the table
customer_segmentation.to_csv(
    r"C:\Users\saumy\OneDrive\Desktop\job courses\New folder\demand forecasting\data\customer_segmentation.csv",
    index=False
)

# 5. Print the results
print("--- Customer Count per Segment ---")
print(customer_segmentation["Customer_Size"].value_counts())

print("\n--- Total Revenue per Segment ---")
revenue_sum = customer_segmentation.groupby("Customer_Size", observed=True)["Total_Revenue"].sum().round(2)
print(revenue_sum)

print(customer_segmentation.head(5))

print("\nDone! Clean boundaries applied.")