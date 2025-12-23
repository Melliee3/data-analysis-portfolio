import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

# 1. Φόρτωμα δεδομένων
df = pd.read_csv("air_quality_data.csv")
df["date"] = pd.to_datetime(df["date"])

# Προαιρετικοί έλεγχοι ποιότητας δεδομένων
# df.info()
# print("nulls:\n", df.isnull().sum())
# print("na:\n", df.isna().sum())
# print("duplicates:\n", df.duplicated().sum())
# print(df.describe())

# 2. Μέση τιμή PM2.5 ανά πόλη
pm_city = df.groupby("city")["pm25"].mean().sort_values(ascending=False)
print("Average PM2.5 per city:\n", pm_city, "\n")

# 3. Υπολογισμός απλού AQI δείκτη (μέσος όρος των ρύπων)
df["AQI_index"] = (
    df["pm25"] + df["no2"] + df["so2"] + df["o3"] + df["co"]
) / 5

max_AQI = df["AQI_index"].max()
min_AQI = df["AQI_index"].min()

highest_AQI = df[df["AQI_index"] == max_AQI][["city", "date", "AQI_index"]]
lowest_AQI = df[df["AQI_index"] == min_AQI][["city", "date", "AQI_index"]]

print("City and date with the highest AQI:\n", highest_AQI, "\n")
print("City and date with the lowest AQI:\n", lowest_AQI, "\n")

# 4. Μέσος AQI ανά πόλη + κατηγορία ποιότητας
overall_AQI_city = df.groupby("city")["AQI_index"].mean().sort_values(ascending=False)

print("Average AQI per city & category:")
for city, value in overall_AQI_city.items():
    if value < 18:
        cat = "Unhealthy"
    elif value < 20:
        cat = "Moderate"
    else:
        cat = "Good"
    print(f"  {city}: {value:.2f} - {cat}")
print()

# 5. Πίνακας συσχέτισης μεταξύ ρύπων
numeric_df = df[["pm25", "no2", "so2", "co", "o3"]]
correlation_matrix = numeric_df.corr()
print("Correlation matrix:\n", correlation_matrix.round(2), "\n")

plt.figure(figsize=(8, 6))
sns.heatmap(
    correlation_matrix,
    annot=True,
    cmap="coolwarm",
    fmt=".2f",
    linewidths=0.5,
    linecolor="black",
)
plt.title("Correlation Between Pollutants", pad=20)
plt.tight_layout()
plt.show()

# 6. Γράφημα: Μέσος AQI ανά πόλη
plt.figure(figsize=(6, 4))
plt.bar(overall_AQI_city.index, overall_AQI_city.values, edgecolor="black")
plt.title("Average AQI per City", pad=20)
plt.xlabel("City")
plt.ylabel("AQI")
plt.grid(axis="y", linestyle="--", alpha=0.5)

for i, v in enumerate(overall_AQI_city.values):
     plt.text(i, v, f"{v:.2f}", ha="center", va="bottom")

plt.tight_layout()
plt.show()
