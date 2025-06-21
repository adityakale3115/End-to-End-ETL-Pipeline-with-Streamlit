import streamlit as st
import sqlite3
import pandas as pd
import plotly.express as px
from datetime import datetime

# Connect to SQLite DB
conn = sqlite3.connect('../database/quantifai.db')
customers = pd.read_sql_query("SELECT * FROM customers", conn)
products = pd.read_sql_query("SELECT * FROM products", conn)
orders = pd.read_sql_query("SELECT * FROM orders", conn)
conn.close()

# Ensure date format for orders
orders['order_date'] = pd.to_datetime(orders['order_date'], errors='coerce')

# -----------------------------
# 🎨 Streamlit UI
st.set_page_config(page_title="Quantifai Dashboard", layout="wide")
st.title("📊 Quantifai Data Dashboard")

# Sidebar Navigation
tab = st.sidebar.radio("Navigate", ["Overview", "Customers", "Orders", "Products"])

# -----------------------------
# 📊 Overview Tab
if tab == "Overview":
    st.header("📌 Summary Metrics")
    col1, col2, col3 = st.columns(3)
    col1.metric("Total Customers", customers.shape[0])
    col2.metric("Total Orders", orders.shape[0])
    col3.metric("Total Products", products.shape[0])

    st.subheader("💸 Top Customers by Spend")
    if "total_spent" in customers.columns:
        top_cust = customers.sort_values("total_spent", ascending=False).head(5)
        st.dataframe(top_cust[["customer_id", "customer_name", "total_spent"]])

    st.subheader("🛒 Top Ordered Products")
    if "product_id" in orders.columns:
        top_prods = orders['product_id'].value_counts().head(5).reset_index()
        top_prods.columns = ['Product ID', 'Orders']
        st.bar_chart(top_prods.set_index('Product ID'))

# -----------------------------
# 👥 Customers Tab
elif tab == "Customers":
    st.header("👥 Customer Details")

    col1, col2 = st.columns(2)
    with col1:
        segment = st.radio("🎯 Filter by Segment", options=["All"] + sorted(customers['segment'].dropna().unique()))
    with col2:
        gender = st.radio("⚧️ Filter by Gender", options=["All"] + sorted(customers['gender'].dropna().unique()))

    # 🔍 Real-time Search
    search_input = st.text_input("🔍 Search by Name or Email")

    # 🧮 Sliders
    col3, col4 = st.columns(2)
    with col3:
        min_orders = st.slider("Min Total Orders", 0, int(customers['total_orders'].max()), 0)
    with col4:
        min_loyalty = st.slider("Min Loyalty Points", 0, int(customers['loyalty_points'].max()), 0)

    # Filter logic
    filtered = customers.copy()
    if segment != "All":
        filtered = filtered[filtered['segment'] == segment]
    if gender != "All":
        filtered = filtered[filtered['gender'] == gender]
    if search_input:
        filtered = filtered[
            filtered['customer_name'].str.contains(search_input, case=False, na=False) |
            filtered['email'].str.contains(search_input, case=False, na=False)
        ]
    filtered = filtered[
        (filtered['total_orders'] >= min_orders) &
        (filtered['loyalty_points'] >= min_loyalty)
    ]

    st.write(f"Showing {filtered.shape[0]} customers matching criteria:")
    st.dataframe(filtered)

    # 📥 Download button
    csv = filtered.to_csv(index=False).encode('utf-8')
    st.download_button("📥 Download Filtered Data", csv, "filtered_customers.csv", "text/csv")

    # 🔍 Dynamic Customer Insights
    if not filtered.empty:
        selected_cust = st.selectbox("📌 Select a Customer to View Details", filtered['customer_name'].unique())
        cust_data = filtered[filtered['customer_name'] == selected_cust].iloc[0]
        st.info(f"""
        **Email**: {cust_data['email']}
        **Status**: {cust_data['status'].title()}
        **Total Orders**: {cust_data['total_orders']}
        **Total Spent**: ₹{cust_data['total_spent']}
        **Loyalty Points**: {cust_data['loyalty_points']}
        """)

    # 📊 Segment Chart
    st.subheader("📊 Segment Distribution")
    st.bar_chart(customers['segment'].value_counts())

    # 🧑 Gender Pie Chart
    st.subheader("🧑 Gender Distribution (Pie Chart)")
    gender_counts = customers['gender'].value_counts().reset_index()
    gender_counts.columns = ['Gender', 'Count']
    fig = px.pie(gender_counts, names='Gender', values='Count', title='Customer Gender Breakdown', hole=0.4)
    st.plotly_chart(fig)

# -----------------------------
# 📬 Orders Tab
elif tab == "Orders":
    st.header("📬 Order Data")

    # 📅 Date Range Filter
    st.subheader("📅 Filter Orders by Date Range")
    min_date = orders['order_date'].min()
    max_date = orders['order_date'].max()
    date_range = st.date_input("Select Date Range", [min_date, max_date])
    mask = (orders['order_date'] >= pd.to_datetime(date_range[0])) & (orders['order_date'] <= pd.to_datetime(date_range[1]))
    filtered_orders = orders[mask]

    st.write(f"Showing {filtered_orders.shape[0]} orders between {date_range[0]} and {date_range[1]}:")
    st.dataframe(filtered_orders)

    col1, col2 = st.columns(2)
    col1.metric("🧾 Total Order Value", f"₹{filtered_orders['total_amount'].sum():,.2f}")
    col2.metric("🧮 Avg Quantity per Order", f"{filtered_orders['quantity'].mean():.2f}")

    # 📊 Payment Method Breakdown
    st.subheader("💳 Payment Methods")
    st.bar_chart(filtered_orders['payment_method'].value_counts())

# -----------------------------
# 📦 Products Tab
elif tab == "Products":
    st.header("📦 Product Listings")

    # Filter by category
    categories = products['category'].dropna().unique().tolist()
    cat_filter = st.selectbox("Filter by Category", options=["All"] + sorted(categories))
    prod_filtered = products.copy()
    if cat_filter != "All":
        prod_filtered = prod_filtered[prod_filtered['category'] == cat_filter]

    # Search product
    search_prod = st.text_input("🔍 Search Product by Name")
    if search_prod:
        prod_filtered = prod_filtered[prod_filtered['product_name'].str.contains(search_prod, case=False, na=False)]

    st.write(f"Showing {prod_filtered.shape[0]} products")
    st.dataframe(prod_filtered)

    # Low Stock Alert
    st.subheader("⚠️ Low Stock Products")
    low_stock = products[products['stock_level'] < products['reorder_level']]
    st.dataframe(low_stock)
