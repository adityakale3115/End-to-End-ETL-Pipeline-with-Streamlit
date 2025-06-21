import pandas as pd
import numpy as np

def clean_order_data(filepath):
    orders = pd.read_csv("../data/orders_unstructured_data.csv")

    # Drop 'ord_id' and 'customer_id' (keep cust_id)
    orders.drop(columns=['ord_id', 'customer_id'], inplace=True)

    # Fill order_date using order_datetime if missing
    orders['order_date'] = orders['order_date'].fillna(orders['order_datetime'])
    orders.drop(columns=['order_datetime'], inplace=True)

    # Normalize date to DD-MM-YYYY
    def parse_date(date_str):
        if pd.isnull(date_str):
            return np.nan
        for fmt in ("%d-%m-%Y", "%d-%m-%Y %H:%M:%S", "%m/%d/%Y", "%Y-%m-%d", "%Y-%m-%d %H:%M:%S"):
            try:
                return pd.to_datetime(date_str, format=fmt).strftime("%d-%m-%Y")
            except:
                continue
        return np.nan

    orders['order_date'] = orders['order_date'].apply(parse_date)

    # Merge 'status' and 'order_status'
    orders['status'] = orders['status'].combine_first(orders['order_status'])
    orders['status'] = orders['status'].str.lower()
    orders.drop(columns=['order_status'], inplace=True)

    orders.reset_index(drop=True, inplace=True)
    return orders
