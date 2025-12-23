import pandas as pd
import matplotlib.pyplot as plt

# 1. Load data
df = pd.read_csv('vgsales.csv')

# 2. Basic data checks (optional)
# df.info()
# print("nulls:\n", df.isnull().sum())
# print("na:\n", df.isna().sum())
# print("duplicates:\n", df.duplicated().sum())
# print(df.describe())
# Note: Some entries have missing Year or Publisher values and may be excluded in specific analyses when needed.

# 3. Basic dataset metrics
platforms_unique = df['Platform'].nunique()
print('Number of different Platforms avaialble:', platforms_unique)

genres_unique = df['Genre'].nunique()
print('Number of different Genres avaialble:', genres_unique)

publishers_unique = df['Publisher'].nunique()
print('Number of different Publishers avaialble:', publishers_unique)

global_sales_sum = df['Global_Sales'].sum()
print(f'Global sales sum: {global_sales_sum:.2f} €')

# 4. Top games / platforms / genres / publishers by Global Sales
top_games = df.groupby('Name')['Global_Sales'].sum().reset_index().sort_values(by='Global_Sales', ascending=False).head(10)
print('Top Games according to Global Sales:\n', top_games)

top_platform = df.groupby('Platform')['Global_Sales'].sum().reset_index().sort_values(by='Global_Sales', ascending=False).head(10)
print('Top Platform according to Global Sales:\n', top_platform)

top_genre = df.groupby('Genre')['Global_Sales'].sum().reset_index().sort_values(by='Global_Sales', ascending=False).head(10)
print('Top Genre according to Global Sales:\n', top_genre)

publisher_sales = df.groupby('Publisher')['Global_Sales'].sum().reset_index().sort_values(by='Global_Sales', ascending=False).head(8)

# 5. Bar charts: Top Platform, Top Genre, Top Publishers
fig, ax = plt.subplots(1, 3, figsize=(18, 6))

for a in ax:
    a.grid(axis='y', linestyle=':', linewidth=0.5)

ax[0].bar(top_platform['Platform'], top_platform['Global_Sales'], edgecolor='black')
ax[0].set_xlabel('Platform')
ax[0].set_ylabel('Global Sales (millions)')
ax[0].set_title('Top Platform according to Global Sales')
ax[0].tick_params(rotation=45)

ax[1].bar(top_genre['Genre'], top_genre['Global_Sales'], edgecolor='black')
ax[1].set_xlabel('Genre')
ax[1].set_title('Top Genre according to Global Sales')
ax[1].tick_params(rotation=45)

ax[2].bar(publisher_sales['Publisher'], publisher_sales['Global_Sales'], edgecolor='black')
ax[2].set_xlabel('Publisher')
ax[2].set_title('Top Publishers', pad=20)
ax[2].tick_params(rotation=45, labelsize=8)

plt.tight_layout()
plt.show()

# 6. Sales per region (Pie chart)
sales = df[['NA_Sales', 'EU_Sales', 'JP_Sales', 'Other_Sales']].sum()
sales = sales.rename({'NA_Sales': 'North America', 'EU_Sales': 'Europe', 'JP_Sales': 'Japan', 'Other_Sales': 'Other'})
print('\n Sales per Region: \n', sales)

plt.figure(figsize=(7, 7))
plt.pie(x=sales.values, labels=sales.index, autopct='%1.1f%%', startangle=90)
plt.axis('equal')
plt.title('Sales per Region', pad=20)
plt.tight_layout()
plt.show()

# 7. Sales per year (Line chart)
# Convert Year to numeric to avoid issues if it's read as object
df['Year'] = pd.to_numeric(df['Year'], errors='coerce')

sales_year = df.groupby('Year')['Global_Sales'].sum().reset_index().sort_values(by='Year', ascending=True)

plt.figure(figsize=(8, 7))
plt.plot(sales_year['Year'], sales_year['Global_Sales'], marker='o', color='red')
plt.title('Sales per Year', pad=20)
plt.xticks(rotation=45)
plt.grid(True)
plt.tight_layout()
plt.show()
