import pandas as pd
import numpy as np
import matplotlib.pyplot as plt

# 1. Φόρτωση δεδομένων & μετατροπή της ημερομηνίας
df = pd.read_csv("sales_data2.csv")
df["date"] = pd.to_datetime(df["date"])

# Έλεγχος ποιότητας δεδομένων (κρατημένο για debug)
# print(df.isna().sum(),
#       'null', df.isnull().sum(),
#       'duplicates', df.duplicated().sum())

# 2. Υπολογισμός εσόδων ανά γραμμή & συνολικών εσόδων
df["revenue"] = df["price"] * df["quantity"]
total_revenue = df["revenue"].sum()
print("Total Revenue:\n", total_revenue)

# 3. Μέσο έσοδο ανά παραγγελία (ίδια τιμή για κάθε γραμμή με ίδιο order_id)
avg_revenue_per_order = (
    df.groupby("order_id")["revenue"]
      .mean()
      .rename("avg_revenue_per_order")
)
df = df.merge(avg_revenue_per_order, on="order_id", how="left")
print(df.head())

# 4. Top 5 προϊόντα με βάση τη συνολική ποσότητα πουλήσεων
sales = (
    df.groupby("product_id")["quantity"]
      .sum()
      .reset_index()
      .sort_values(by="quantity", ascending=False)
)
top_products = sales.head(5)
print("Products with the most sales:\n", top_products)

# 5. Γραμμικό γράφημα: έσοδα ανά μέρα
plt.plot(df["date"], df["revenue"])
plt.title("Revenue per Day")
plt.xlabel("Date")
plt.ylabel("Revenue")
plt.xticks(rotation=45)
plt.tight_layout()
plt.show()
