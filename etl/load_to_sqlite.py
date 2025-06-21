import sqlite3
import os

# Import your cleaning functions
from transform_customers import clean_customer_data
from transform_products import clean_product_data
from transform_orders import clean_order_data

# Define paths to raw data
customer_path = os.path.join("..", "data", "customers_messy_data.json")
product_path = os.path.join("..", "data", "products_inconsistent_data.json")
order_path = os.path.join("..", "data", "orders_unstruct_data.csv")

# Step 1: Clean all data
customers = clean_customer_data(customer_path)
products = clean_product_data(product_path)
orders = clean_order_data(order_path)

# Step 2: Save cleaned data into SQLite
db_path = os.path.join("..", "database", "quantifai.db")
conn = sqlite3.connect(db_path)

# Load into tables
customers.to_sql("customers", conn, index=False, if_exists='replace')
products.to_sql("products", conn, index=False, if_exists='replace')
orders.to_sql("orders", conn, index=False, if_exists='replace')

conn.close()
print("All tables loaded into SQLite successfully!")
