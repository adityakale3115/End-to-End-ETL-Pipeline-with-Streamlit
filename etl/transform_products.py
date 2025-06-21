import pandas as pd

def clean_product_data(filepath):
    products = pd.read_json("../data/products_inconsistent_data.json")

    # Drop 'item_id' and 'item_name'
    products.drop(columns=['item_id', 'item_name'], inplace=True)

    # Drop 'product_category' (keep only 'category')
    products.drop(columns=['product_category'], inplace=True)

    # Clean 'is_active' column to Boolean
    products['is_active'] = products['is_active'].astype(str).str.lower().map({
        'yes': True, 'true': True, '1': True,
        'no': False, 'false': False, '0': False
    })

    products.reset_index(drop=True, inplace=True)
    return products
