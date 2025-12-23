import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

# --------------------------------------------------
# Load & preprocess data
# --------------------------------------------------
df = pd.read_csv('finance_liquor_sales.csv')

df['date'] = pd.to_datetime(df['date'])
df['year'] = df['date'].dt.year

# Handle missing values
df['store_location'] = df['store_location'].fillna('Unknown')
df['category'] = df['category'].fillna('Unknown')
df['category_name'] = df['category_name'].fillna('Unknown')
df['county'] = df['county'].fillna('Unknown')

# Keep selected years
df = df[df['year'].between(2016, 2019)]
df.drop(columns='date', inplace=True)

# --------------------------------------------------
# Task 1: Top-selling item per ZIP code
# --------------------------------------------------
sales_zip_item = (df.groupby(['zip_code', 'item_number'])['bottles_sold'].sum().reset_index())

# Select top item per ZIP
top_sales_zip = (sales_zip_item
                 .loc[sales_zip_item.groupby('zip_code')['bottles_sold'].idxmax()]
                 .sort_values('bottles_sold', ascending=False)
                 .reset_index(drop=True))

top5 = top_sales_zip.head(5)

# Scatter plot
item_color = top_sales_zip['item_number'].astype('category').cat.codes

plt.figure(figsize=(8, 6))
plt.scatter(top_sales_zip['zip_code'],top_sales_zip['bottles_sold'],
            s=top_sales_zip['bottles_sold'],
            c=item_color,
            cmap='tab20',
            alpha=0.7)

# Annotate top 5 items
for index, row in top5.iterrows():
    plt.annotate(text=row['item_number'],xy=(row['zip_code'], row['bottles_sold']),
                xytext=(10, 5),
                textcoords='offset points',
                ha='center',
                va='bottom')

plt.xlabel('ZIP Code')
plt.ylabel('Bottles Sold')
plt.title('Top-Selling Items per ZIP Code')
plt.show()

# --------------------------------------------------
# Pie chart: Top 5 items by bottles sold
# --------------------------------------------------
plt.pie(top5['bottles_sold'],labels=top5['item_number'],
        autopct='%1.2f%%',
        startangle=90,
        colors=['#4E79A7', '#F28E2B', '#59A14F', '#E15759', '#B07AA1'],
        wedgeprops={'edgecolor': 'white', 'linewidth': 0.5})

plt.axis('equal')
plt.title('Top Items by Bottles Sold', pad=20)
plt.show()

# --------------------------------------------------
# Task 2: Market share by store
# --------------------------------------------------
stores_sales = df.groupby('store_name')['sale_dollars'].sum()
total_sales = stores_sales.sum()

percent_sales = ((stores_sales / total_sales * 100).round(2)
                 .reset_index(name='percent_sales')
                 .sort_values('percent_sales', ascending=False).head(20))

# Horizontal bar chart
fig, ax = plt.subplots(figsize=(12, 7))
sns.barplot(x='percent_sales',y='store_name',data=percent_sales,
            hue='store_name',
            palette='tab20',
            legend=False)

ax.set_title('% Sales by Store', pad=20)
ax.set_xlabel('Sales (%)', labelpad=10)
ax.set_ylabel('Store Name', labelpad=10)
ax.tick_params(axis='y', labelsize=9)

for container in ax.containers:
    ax.bar_label(container, fmt='%.2f%%', padding=2)

plt.tight_layout()
plt.show()

# --------------------------------------------------
# Cumulative sales share (Top 10 stores)
# --------------------------------------------------
percent_sales['cumulative_percent'] = percent_sales['percent_sales'].cumsum()
top10 = percent_sales['cumulative_percent'].head(10).reset_index(drop=True)

plt.figure(figsize=(8, 6))
plt.plot(top10.index + 1,top10.values,
         marker='o',
         color='#695F8C')

plt.axhline(y=50, label='50% cumulative sales',
            color='#CB011C',
            linestyle='--',
            linewidth=1)

plt.xlabel('Rank', labelpad=10)
plt.ylabel('Cumulative Percent', labelpad=10)
plt.title('Cumulative Sales Share of Top Stores', pad=10)
plt.grid(True, linestyle=':')
plt.legend()

# Annotate points
for x, y in zip(top10.index + 1, top10.values):
    plt.text(x+1, y - 1, f'{y:.1f}%', ha='center', va='bottom')

plt.show()
