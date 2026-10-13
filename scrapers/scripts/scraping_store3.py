"""
00c. Supermarket data project - scraper store 3

Date created: 13 October 2026
Last updated: 13 October 2026

author: Carlos Restituyo


This script collects price and product data from a Dominican supermarket website.
Using API requests, we ask the server for many product pages in the site, receiving the
product information in JSON. This is then turned into a dataframe and then exported to
a local Postgres database.

"""

import base64
import json
import requests
import pandas as pd
from sqlalchemy import create_engine, text, inspect
import datetime
import numpy as np
from scripts.env_vars import PG_HOST, PG_USER, PG_PASSWORD, PG_DATABASE, PG_PORT, STORE3_STARTLINK, STORE3_HOST, STORE3_AUTH
from scripts.utils import clean_html, flatten_json
import re
import time

def main():
    url = STORE3_STARTLINK
    
    # Query parameters template
    
    params = {
        "model.filterByIdTienda":"1000",
        "paginationMaxItems":"30",
        "paginationOffset":"0", #paginationMaxItems x1,2,3
        "model.filterByIdSeccion":"3", #value here is 3 for store, 4 for pet shop, 5 for pharmacy
        "showOrder":"importerankingArticulo asc,bravoArticulo desc,nombreArticulo asc",
    }
    
    headers = {
        "Accept-Encoding":"gzip",
        "Host":STORE3_HOST,
        "User-Agent":"okhttp/4.12.0",
        "X-Auth-Token":STORE3_AUTH,
            }
    
    all_products = []
    
    #have to loop over values 3,4,5; for each, request paginationoffsets starting 0, until the thing fails
    #until len(data['data']['list']) == 0
    for section in [3,4,5,7,8,9,11,12,13,14,15,16,17,18,19,20,1031,1098,1097,1096,1021,1095,1093,
                    1023,1019,1065,1020,1018,1026,1016,1024,1022,1017,1056]:
        time.sleep(5)
        print(f"In section ID: {section}")
        for page in range(0,301):
            print(f"In Page: {page}")
            #start page 0, first page
            page_offset = page*30
            #pass it to the parameters dict
            params['paginationOffset'] = f'{page_offset}'
            #also pass section
            params['model.filterByIdSeccion'] = f'{section}'
            #make initial request
            response = requests.get(url, params=params, headers = headers)
            #get the data from the request
            data = response.json()
            #get the data out of the response object
            products = data.get("data", {})
            if len(products['list'])>0:
                #append it to all_products
                all_products.extend(products['list'])
            else:
                print("Done here...")
                break
            time.sleep(5)
    
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
                            'nombrearticulo':'product_name',
                            'idarticulo':'product_id',
                            'idexternoarticulo':'product_sku',
                            'associatedtienda_0_pvparticulotienda':'price',
                            'metatagarticulo':'description',
                            'associatedpvp':'listprice',
                            'originalpvp':'originalprice',
                            })
    
    df['sku'] = df['product_sku']
    df['scrape_datetime'] = datetime.datetime.now()
    df['offer_availability'] = np.where(df['associatedtienda_0_disponiblearticulotienda'] == True, 'In Stock', 'Out of Stock')
    
    #Data export
    #homogenize the names and then export to postgres database
    #this must match the amount of columns we will produce from the flattened json
    
    
    conn_string = f'postgresql+psycopg://{PG_USER}:{PG_PASSWORD}@{PG_HOST}:{PG_PORT}/{PG_DATABASE}'
    db = create_engine(conn_string)
    
    with db.begin() as conn:
        store3_table = text('''CREATE TABLE IF NOT EXISTS rawdata.store3(scrape_datetime timestamp, product_id text,
        product_name text, description text, sku text, brand_name text, listprice float, originalprice float,
        price float, offer_availability text, product_sku text);''')
        conn.execute(store3_table)
    
    #export subset of columns specifically for price tracker
    df[['scrape_datetime', 'product_id', 'product_name', 'description',
        'sku', 'listprice', 'originalprice', 'price',
        'offer_availability', 'product_sku']].to_sql('store3', db, if_exists= 'append',index=False, schema = 'rawdata')
    
    #save a full version of the data in case we want to extend analysis later on
    inspector = inspect(db)
    if inspector.has_table('store3_full', schema = 'rawdata'):
        db_cols = [col["name"] for col in inspector.get_columns('store3_full', schema = 'rawdata')]
        df.reindex(columns=db_cols).to_sql('store3_full', db, if_exists='append', index=False, schema = 'rawdata')
    else:
        df.to_sql('store3_full', db, if_exists='append', index=False, schema = 'rawdata')