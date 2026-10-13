"""
00a. Supermarket data project - scraper store 1

Date created: 19 August 2026
Last updated: 29 September 2026

author: Carlos Restituyo


This script collects price and product data from a Dominican supermarket website.
Using BeautifulSoup, the scraper lifts data directly from the website html, and
crawls through all internal links starting from the landing page until all store web
links have been crawled.

"""


import pandas as pd
import random
from sqlalchemy import create_engine, text
import datetime
from scripts.env_vars import PG_HOST, PG_USER, PG_PASSWORD, PG_DATABASE, PG_PORT, STORE1_STARTLINK
from scripts.utils import getLinks

def main():
    #collect data
    pages=set()
    product_data = []
    random.seed(1234556)

    getLinks(STORE1_STARTLINK, pages, product_data)

    titles=['scraped_site','product_id','product_name','price','product_sku']

    df = pd.DataFrame(product_data, columns= titles)
    df['scrape_datetime'] = datetime.datetime.now()
    df['price'] =pd.to_numeric(df.price, errors="coerce")

    #export to postgresql database
    # establish connections
    conn_string = f'postgresql+psycopg://{PG_USER}:{PG_PASSWORD}@{PG_HOST}:{PG_PORT}/{PG_DATABASE}'
    db = create_engine(conn_string)

    with db.begin() as conn:

        store1_table = text('''CREATE TABLE IF NOT EXISTS rawdata.store1(scraped_site text,scrape_datetime timestamp, product_id text,
                            product_name text,price float, product_sku text);''')
        conn.execute(store1_table)


    df.to_sql('store1', db, if_exists= 'append', index=False, schema = 'rawdata')
