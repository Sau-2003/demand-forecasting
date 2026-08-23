import pandas as pd
import numpy as np

# 1. Read the customer-stock summary
df = pd.read_csv(
    r"C:\Users\saumy\OneDrive\Desktop\job courses\New folder\demand forecasting\data\2.customer_stock_summary.csv",
    encoding="cp1252"
)

# 2. Sum Total Revenue for each unique CustomerID
customer_segmentation = (
    df.groupby("CustomerID", dropna=False)["Total_Revenue"]
    .sum()
    .reset_index()
)

customer_segmentation["Total_Revenue"] = (
    customer_segmentation["Total_Revenue"].round(2)
)

# 3. Apply the clean custom bins
custom_bins = [-np.inf, 3500, 40000, np.inf]
segment_labels = ["Small", "Medium", "Large"]

customer_segmentation["Customer_Size"] = pd.cut(
    customer_segmentation["Total_Revenue"],
    bins=custom_bins,
    labels=segment_labels
)

# 4. Save the table
output_path = r"C:\Users\saumy\OneDrive\Desktop\job courses\New folder\demand forecasting\data\2.customer_segmentation.csv"


# 5. Print the results
print(customer_segmentation.head(5))
print(f"\nDone! Clean boundaries applied.")