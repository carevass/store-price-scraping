"""
01. Supermarket data project - cleaning & transformaion

Date created: 19 August 2026
Last updated: 13 October 2026

author: Carlos Restituyo


This takes in raw data scraped from supermarket websites on products, cleans and tranforms
the data into tables to be exported back to Postgres to be used in making dashboards.

"""

#%% Preliminaries
#%%% Packages
from sqlalchemy import create_engine, text
from scripts.env_vars import PG_HOST, PG_USER, PG_PASSWORD, PG_DATABASE, PG_PORT
from scripts.utils import clean_data, categorize_products, categorize_store_brand

import pandas as pd
import warnings

def main():
    #%%% Connections
    conn_string = f'postgresql+psycopg://{PG_USER}:{PG_PASSWORD}@{PG_HOST}:{PG_PORT}/{PG_DATABASE}'
    db = create_engine(conn_string)


    #eventually have this iterate over a list of tables
    store1 = clean_data('store1', db)

    store2 = clean_data('store2', db)
    
    store3 = clean_data('store3', db)
    # append data
    sm_data = pd.concat([store1,store2,store3], ignore_index = True)

    sm_data['category'] = sm_data['product_name'].apply(categorize_products)
    sm_data['store_brand'] = sm_data['product_name'].apply(categorize_store_brand)
    #sm_data[['product_name']].sample(n = 1000, random_state = 541557).to_csv('proc/training_data.csv', index = False)

    #this x must be 0 eventually
    if len(sm_data[sm_data.category.isna()][['product_name', 'category']]) > 0:
        warnings.warn('''You have uncategorized products in your data, eventually you will need to finish
                    categorizing these products to use them in analysis.''')



    #%% Export data
    #prepare the queries to create the tables we will use


    with db.begin() as conn:
        # Wrap your string with text()
        store_table = text('CREATE TABLE IF NOT EXISTS proc.store_info(supermarket_id text primary key, supermarket_name text)')
        product_table = text('''CREATE TABLE IF NOT EXISTS proc.product_info(supermarket_id text, hashed_product text primary key,
                                product_name text, category text, store_brand smallint)''')
        price_table = text('CREATE TABLE IF NOT EXISTS proc.product_prices(hashed_product text, price float, scrape_date date)')
        # Execute and fetch results
        conn.execute(store_table)
        conn.execute(product_table)
        conn.execute(price_table)



    #export products table
    sm_data[['hashed_product', 'price', 'scrape_date']].to_sql('product_prices', db, if_exists= 'delete_rows',index=False, schema = 'proc')

    #export store table
    sm_data.drop_duplicates(subset = ['supermarket_name'])[['supermarket_id',
                                                            'supermarket_name']].to_sql('store_info', db, if_exists= 'delete_rows',index=False, schema = 'proc')

    #export products table
    sm_data.drop_duplicates(subset = ['hashed_product'])[['supermarket_id','hashed_product',
                                                        'product_name', 'category','store_brand']].to_sql('product_info', db, if_exists= 'delete_rows',index=False, schema = 'proc')
