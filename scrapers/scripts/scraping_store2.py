import base64
import json
import requests
import pandas as pd
import html
from bs4 import BeautifulSoup
import re
from sqlalchemy import create_engine, text, inspect
import datetime
import numpy as np
from env_vars import PG_HOST, PG_USER, PG_PASSWORD, PG_DATABASE, PG_PORT, STORE2_STARTLINK

#functions

def clean_html(text):
    if not isinstance(text, str):
        return text
    # Convert HTML entities like &lt; and &quot; into actual characters < and "
    unescaped = html.unescape(text)
    # Strip out all HTML tags to leave pure, plain text
    soup = BeautifulSoup(unescaped, "html.parser")
    return soup.get_text(separator=' ', strip=True)

# Function to flatten nested dictionaries
def flatten_json(y):
    out = {}

    def flatten(x, name=''):
        if type(x) is dict:
            for a in x:
                flatten(x[a], name + a + '_')
        elif type(x) is list:
            i = 0
            for a in x:
                flatten(a, name + str(i) + '_')
                i += 1
        else:
            out[name[:-1]] = x

    flatten(y)
    return out

# Base endpoint from your XHR trace
url = STORE2_STARTLINK

# Query parameters template
params = {
    "workspace": "master",
    "maxAge": "short",
    "appsEtag": "remove",
    "domain": "store",
    "locale": "es-DO",
    "__bindingId": "0f7c8c48-1ed8-48c0-b2df-684ad0831aa7",
    "operationName": "productSearchV3",
    "variables": "{}",
    "extensions": json.dumps({
        "persistedQuery": {
            "version": 1,
            "sha256Hash": "b398fc0a2fd04ea5d4f7a94c732c10fb1bf64f8f9a2b31c92aee6a5e796457c9",
            "sender": "vtex.store-resources@0.x",
            "provider": "vtex.search-graphql@0.x"
        }
    })
}

# The JSON structure required by VTEX
payload = {
    "skusFilter": "ALL_AVAILABLE",
    "simulationBehavior": "default",
    "installmentCriteria": "MAX_WITHOUT_INTEREST",
    "productOriginVtex": True,
    "map": "c",
    "query": "supermercado",
    "orderBy": "OrderByScoreDESC",
    "selectedFacets": [{"key": "c", "value": "supermercado"}],
    "operator": "and",
    "fuzzy": "0",
    "searchState": None,
    "hideUnavailableItems": False,
    "facetsBehavior": "Static",
    "categoryTreeBehavior": "default",
    "withFacets": False,
    "from": 0,
    "to": 49  # Request 50 items per batch
}

all_products = []
page_size = 50


for page in range(220):  # Fetch up to 11,000 products
    payload["from"] = page * page_size
    payload["to"] = ((page + 1) * page_size) - 1

    # VTEX requires the variable object to be base64-encoded inside extensions.variables
    #every iteration we have to update the payload dict and declare a new variables value 
    #with the base64 encoding to fetch the next page
    encoded_vars = base64.b64encode(json.dumps(payload).encode()).decode()
    
    extensions = json.loads(params["extensions"])
    extensions["variables"] = encoded_vars
    
    #json dumps turns the new extensions values to json and puts it back in params
    params["extensions"] = json.dumps(extensions)

    response = requests.get(url, params=params)
    data = response.json()

    # Extract products array
    try:
        products = data.get("data", {}).get("productSearch", {}).get("products", [])
    except AttributeError:
        "AttributeError detected. Probably request produced an error and data came back empty. Skipping..."
    if not products:
        print("No more products found.")
        break

    all_products.extend(products)
    print(f"Fetched page {page + 1} ({len(products)} products). Total so far: {len(all_products)}")

print(f"Done! Collected {len(all_products)} total products.")
## shape and cleaning

#fully flatten the df, many columns have nested lists of dicts, we need to flatten such that every key is a separate df column

flattened_context = flatten_json(all_products)

rows = {}

for key, value in flattened_context.items():
    # Regex splits '0_productid' into row index '0' and clean column 'productid'
    match = re.match(r'^(\d+)_(.*)$', key)
    if match:
        row_idx, col_name = match.groups()
        row_idx = int(row_idx)
        
        if row_idx not in rows:
            rows[row_idx] = {}
        
        # Store clean column name without the '0_' prefix
        rows[row_idx][col_name] = value

# Convert the list of clean dictionaries directly into a DataFrame
df = pd.DataFrame(list(rows.values())).dropna(axis=1, how='all')
df.columns = df.columns.str.lower()

df = df.rename(columns = {
                                             'productname':'product_name', 
                                             'productid':'product_id', 
                                             'items_0_itemid':'product_sku',
                                             'items_0_sellers_0_commertialoffer_price':'price',
                                             'items_0_referenceid_0_value':'mpn',
                                             'brand':'brand_name',
                                             'pricerange_sellingprice_highprice':'highprice',
                                             'pricerange_sellingprice_lowprice':'lowprice',
                                             'items_0_sellers_0_commertialoffer_pricevaliduntil':'offer_pricevaliduntil'})



if 'description' in df.columns:
    df['description'] = df['description'].apply(clean_html)
df['sku'] = df['product_sku']
df['scrape_datetime'] = datetime.datetime.now()
df['offer_availability'] = np.where(df['items_0_sellers_0_commertialoffer_availablequantity'] > 0, 'In Stock', 'Out of Stock')
df['offer_pricevaliduntil'] = pd.to_datetime(df['offer_pricevaliduntil'])

#Data export
#homogenize the names and then export to postgres database
#this must match the amount of columns we will produce from the flattened json

    
conn_string = f'postgresql+psycopg://{PG_USER}:{PG_PASSWORD}@{PG_HOST}:{PG_PORT}/{PG_DATABASE}'    
db = create_engine(conn_string)

with db.begin() as conn:
    store2_table = text('''CREATE TABLE IF NOT EXISTS rawdata.store2(scrape_datetime timestamp, product_id text, 
    product_name text, description text, mpn text, sku text, brand_name text, lowprice float, highprice float, 
    price float, offer_availability text, product_sku text, offer_pricevaliduntil timestamp);''')
    conn.execute(store2_table)

#export subset of columns specifically for price tracker
df[['scrape_datetime', 'product_id', 'product_name', 'description', 
    'mpn', 'sku', 'brand_name', 'lowprice', 'highprice', 'price',
    'offer_availability', 'product_sku', 'offer_pricevaliduntil']].to_sql('store2', db, if_exists= 'append',index=False, schema = 'rawdata')

#save a full version of the data in case we want to extend analysis later on
inspector = inspect(db)
if inspector.has_table('store2_full', schema = 'rawdata'):
    db_cols = [col["name"] for col in inspector.get_columns('store2_full', schema = 'rawdata')]
    


df.reindex(columns=db_cols).to_sql('store2_full', db, if_exists='append', index=False, schema = 'rawdata')
