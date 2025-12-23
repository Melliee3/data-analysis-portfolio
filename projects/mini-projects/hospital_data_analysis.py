import pandas as pd
import matplotlib.pyplot as plt
import numpy as np

# 1) Load data
df = pd.read_csv("hospital_admissions_data.csv")

# basic data checks
# df.info()
# print("nulls:\n", df.isnull().sum())
# print("na:\n", df.isna().sum())
# print("duplicates:\n", df.duplicated().sum())
# print(df.describe())

# 2) Parse dates
df['admission_date'] = pd.to_datetime(df['admission_date'])
df['discharge_date'] = pd.to_datetime(df['discharge_date'])

# 3) Feature engineering: stay duration
df['stay_duration'] = df['discharge_date'] - df['admission_date']
df['stay_days'] = df['stay_duration'].dt.days   # numeric version (days)

# 4) Average stay per diagnosis (metric)
stay_per_diagnosis = (df.groupby('diagnosis')['stay_days'].mean().reset_index().sort_values(by='stay_days', ascending=False))
print('\nAverage stay (days) per diagnosis:\n', stay_per_diagnosis)

# 5) Diagnosis frequency
frequency_diagnosis = (df.groupby('diagnosis')['diagnosis'].count().sort_values())
print('\nDiagnosis with the highest frequency:\n', frequency_diagnosis.head())

# 6) Age groups (as defined by you)
age_bins = [0, 20, 35, 50, 60, 100]
df['age_groups'] = pd.cut(df['age'],bins=age_bins, labels=['0-20', '21-35', '36-50', '51-65', '60+'])

stay_per_age = (df.groupby('age_groups', observed=False)['stay_days'].mean().sort_values(ascending=False))
print('\nAverage stay per age group:\n', stay_per_age)

# 7) Bar chart: AVERAGE stay per diagnosis (final version)
plt.figure(figsize=(10, 5))
plt.bar(stay_per_diagnosis['diagnosis'],stay_per_diagnosis['stay_days'],edgecolor='black')
plt.xlabel('Diagnosis')
plt.ylabel('Average Stay (Days)')
plt.title('Average Duration of Stay per Diagnosis')
plt.xticks(rotation=45)
plt.tight_layout()
plt.show()

# 8) Histogram: distribution of stay length
plt.figure(figsize=(8, 6))
plt.hist(df['stay_days'], bins=4, edgecolor='black')
plt.xlabel('Days')
plt.ylabel('Frequency', labelpad=15)
plt.title('Histogram of Stay Duration (Days)', pad=20)
plt.tight_layout()
plt.show()
