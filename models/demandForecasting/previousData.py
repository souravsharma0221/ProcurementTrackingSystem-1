from database.database import conn
from sqlalchemy import text
import pandas as pd
import json
import numpy as np

# Query distinct product IDs from orders table
product_ids = conn.execute(text('SELECT id FROM products')).fetchall()
product_ids = [product_id[0] for product_id in product_ids]

# Create empty summary table with product IDs as columns
summary_columns = ['year_month'] + product_ids
summary = pd.DataFrame(columns=summary_columns)

# Query data from orders table
result=conn.execute(text('SELECT order_time, product_id FROM orders')).fetchall()
df = pd.DataFrame(result)

# Convert order_time to datetime and extract year and month
df['order_time'] = pd.to_datetime(df['order_time'])
df['year_month'] = df['order_time'].dt.strftime('%Y-%m')

# Deserialize product_id column to a list of integers
df['product_id'] = df['product_id'].apply(lambda x: json.loads(x))

# Split product_id column into separate rows for each product ID
df = df.explode('product_id')

# Pivot table to summarize data by year_month and product_id
summary_data = df.pivot_table(index='year_month', columns='product_id', aggfunc='size').reset_index()
summary_data.columns = summary.columns

# Convert summary data to numeric data types
summary_data = summary_data.astype({col: np.float64 for col in summary_data.columns if col != 'year_month'})

# Fill NaN values with 0
summary_data = summary_data.fillna(0)

# Append summary data to summary table
data_frame = summary.append(summary_data, ignore_index=True)




