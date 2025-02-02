import pandas as pd
import matplotlib.pyplot as plt

# Load dataset
df = pd.read_csv('superstore_sales.csv')
df['Order Date'] = pd.to_datetime(df['Order Date'])

# Year-over-Year (YoY) Growth Analysis
df['Year'] = df['Order Date'].dt.year
yearly_sales = df.groupby('Year')['Sales'].sum().reset_index()
yearly_sales['YoY Growth'] = yearly_sales['Sales'].pct_change() * 100

# Regional Sales Analysis
regional_sales = df.groupby('Region')['Sales'].sum().sort_values(ascending=False).reset_index()

# Customer Segmentation (RFM Analysis)
snapshot_date = df['Order Date'].max() + pd.DateOffset(days=1)
rfm = df.groupby('Customer ID').agg({
    'Order Date': lambda x: (snapshot_date - x.max()).days,  # Recency
    'Order ID': 'count',                                      # Frequency
    'Sales': 'sum'                                            # Monetary
}).rename(columns={
    'Order Date': 'Recency',
    'Order ID': 'Frequency',
    'Sales': 'Monetary'
})

# Save cleaned data for Power BI
df.to_csv('cleaned_sales_data.csv', index=False)

# Generate visualizations
plt.figure(figsize=(12, 6))
plt.bar(yearly_sales['Year'], yearly_sales['Sales'], color='skyblue')
plt.title('Yearly Sales Trends')
plt.xlabel('Year')
plt.ylabel('Total Sales ($)')
plt.savefig('visualizations/yearly_sales.png')

plt.figure(figsize=(12, 6))
plt.bar(regional_sales['Region'], regional_sales['Sales'], color='orange')
plt.title('Regional Sales Performance')
plt.xticks(rotation=45)
plt.ylabel('Total Sales ($)')
plt.savefig('visualizations/regional_sales.png')