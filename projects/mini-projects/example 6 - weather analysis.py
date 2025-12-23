import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import plotly.express as px   # σωστό import για Plotly Express

# 1. Φόρτωση δεδομένων & μετατροπή της ημερομηνίας
df = pd.read_csv("weather_data.csv")
df["date"] = pd.to_datetime(df["date"])

# Προαιρετικοί έλεγχοι ποιότητας δεδομένων (κρατημένοι για debug)
# print(df.info())
# print("nulls:", df.isnull().sum())
# print("na:", df.isna().sum())
# print("duplicates:", df.duplicated().sum())

# 2. Υπολογισμός μέσης θερμοκρασίας ημέρας
df["avg_temp"] = (df["min_temp"] + df["max_temp"]) / 2

# 3. Εξαγωγή στοιχείων ημερομηνίας & μηνιαία μέση θερμοκρασία
df["month"] = df["date"].dt.month
df["year"] = df["date"].dt.year
df["day"] = df["date"].dt.day

avg_monthly = (
    df.groupby(["year", "month"])["avg_temp"]
      .mean()
      .reset_index()
)
print("Average monthly temperature:")
print(avg_monthly)

# 4. Εύρεση πιο ζεστής και πιο κρύας ημέρας
hottest = df["avg_temp"].max()
hottest_day = df[df["avg_temp"] == hottest].iloc[0]["date"]
print(f"Hottest day: {hottest_day.date()} with avg_temp {hottest:.2f}")

coldest = df["avg_temp"].min()
coldest_day = df[df["avg_temp"] == coldest].iloc[0]["date"]
print(f"Coldest day: {coldest_day.date()} with avg_temp {coldest:.2f}")

# 5. Γραμμικό γράφημα: μέση θερμοκρασία ανά ημέρα
plt.plot(df["date"], df["avg_temp"], marker="o")
plt.title("Average Temperature per Day")
plt.xlabel("Date")
plt.ylabel("Average Temperature")
plt.xticks(rotation=45)
plt.grid()
plt.tight_layout()
plt.show()

# 6. Grouped bar chart: min & max θερμοκρασία ανά ημέρα (Plotly Express)
fig = px.bar(
    df,
    x="date",
    y=["min_temp", "max_temp"],
    barmode="group",
    title="Min and Max Temperature per Day"
)
fig.show()