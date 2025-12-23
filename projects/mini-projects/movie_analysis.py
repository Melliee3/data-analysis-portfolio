import pandas as pd
import numpy as np
import matplotlib.pyplot as plt

# -----------------------------------------------------------
# 1. Load the Dataset
# -----------------------------------------------------------
df = pd.read_csv("movies.csv")
# Uncomment only when you want to inspect:
print(df.info())
print(df.head())
# -----------------------------------------------------------
# 2. Basic Cleaning Check (NA, nulls, duplicates)
# -----------------------------------------------------------
# Check for missing values
print(df.isna().sum())
# Check duplicates in rows
print("Duplicates:", df.duplicated().sum())
# Dataset is clean. No further action needed.
# -----------------------------------------------------------
# 3. Compute New Feature — Profit
# -----------------------------------------------------------
# Profit = Revenue - Budget
df['profit'] = df['revenue'] - df['budget']
# Uncomment for debugging:
print(df[['title', 'budget', 'revenue', 'profit']].head())
# -----------------------------------------------------------
# 4. Find Top 5 Movies by Profit
# -----------------------------------------------------------
top_5 = df.sort_values(by='profit', ascending=False).head(5)
# Debug print:
print(top_5[['title', 'profit']])
# -----------------------------------------------------------
# 5. Bar Chart — Top 5 Profit
# -----------------------------------------------------------
plt.figure(figsize=(10, 5))

plt.bar(top_5['title'], top_5['profit'], color='pink', width=0.4)
plt.title('Top 5 Profit')
plt.xlabel('Title')
plt.ylabel('Profit')
# Make Y-axis show full numbers instead of scientific notation (e.g., 1e9)
plt.ticklabel_format(style='plain', axis='y')
# Rotate X labels so long titles are readable
plt.xticks(rotation=45, ha='right', fontsize=8)
plt.tight_layout()
plt.show()
# -----------------------------------------------------------
# 6. Scatter Plot — Budget vs Revenue
# -----------------------------------------------------------
plt.figure(figsize=(7, 5))

plt.scatter(df['budget'], df['revenue'], color='skyblue', alpha=0.7)
plt.title('Budget vs Revenue')
plt.xlabel('Budget')
plt.ylabel('Revenue')
plt.ticklabel_format(style='plain', axis='both')
plt.tight_layout()
plt.show()
