import pandas as pd
import numpy as np

def clean_customer_data(filepath):
    customers = pd.read_json(filepath)

    # --- CLEANING LOGIC ---

    # 1. Drop cust_id (serial)
    customers.drop(columns=['cust_id'], inplace=True)

    # 2. Merge customer_name and full_name
    customers['customer_name'] = customers['customer_name'].combine_first(customers['full_name'])
    customers.drop(columns=['full_name'], inplace=True)

    # 3. Rename 'phone' to 'alternate_phone'
    customers.rename(columns={'phone': 'alternate_phone'}, inplace=True)

    # 4. Use 'reg_date' instead of 'registration_date'
    customers['registration_date'] = customers['reg_date']
    customers.drop(columns=['reg_date'], inplace=True)

    # 5. Merge emails
    customers['email'] = customers['email'].combine_first(customers['email_address'])
    customers.drop(columns=['email_address'], inplace=True)

    # 6. Merge statuses and lowercase
    customers['status'] = customers['status'].combine_first(customers['customer_status'])
    customers['status'] = customers['status'].astype(str).str.lower()
    customers.drop(columns=['customer_status'], inplace=True)

    # 7. Fix customer_name if email leaked into it
    email_mask = customers['customer_name'].str.contains('@', na=False)
    empty_email = customers['email'].isna() | (customers['email'] == '')
    customers.loc[email_mask & empty_email, 'email'] = customers.loc[email_mask & empty_email, 'customer_name']
    customers.loc[email_mask, 'customer_name'] = np.nan
    customers['customer_name'] = customers['customer_name'].fillna('Unknown')

    # 8. Standardize gender values
    customers['gender'] = customers['gender'].astype(str).str.strip().str.lower().map({
        'm': 'M', 'male': 'M',
        'f': 'F', 'female': 'F',
        'o': 'O', 'other': 'O'
    })

    # 9. Reset index
    customers.reset_index(drop=True, inplace=True)

    return customers
