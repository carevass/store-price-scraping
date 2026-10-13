"""
Supermarket data project - scraping & cleaning utils

This script covers utilities to complete the data extraction and cleaning for supermarket prices.
"""
#common packages
from bs4 import BeautifulSoup
import re
import pandas as pd

#for store 1 scraping
from urllib.request import urlopen
from urllib.error import URLError

#for store 2 scraping
import html

#for data cleaning
import hashlib
from unidecode import unidecode
from scripts.consts import store_dict, classification_dict, pattern, pattern2, store_brand


#%%% Functions
def get_hash(text):
    hash_object = hashlib.md5(text.encode())
    return hash_object.hexdigest()

def clean_data(table_name:str, db):
    data = pd.read_sql_query(f'SELECT * FROM rawdata.{table_name}', db)
    data['supermarket_name'] = f'{table_name}'
    data['supermarket_id'] = data['supermarket_name'].map(store_dict)

    #2. hash product names
    data['product_name_id'] = data['product_name'] + data['product_id']
    data['hashed_product'] = data['product_name_id'].apply(get_hash)
    if table_name == 'nacional':
        #special cleaning for nacional, we added scraped site after starting scraping so we are backfilling these values for the same products as before

        group_cols = ["hashed_product"]
        data["scraped_site"] = (
            data.groupby(group_cols)["scraped_site"].bfill()
        )

    #1. remove same-day duplicates
    data['scrape_date'] = pd.to_datetime(data['scrape_datetime']).dt.date
    #use all columns except price to consider duplicates
    data = data.sort_values('scrape_datetime').drop_duplicates(subset=data.columns.difference(['price','scrape_datetime','scraped_site',"product_sku"]),
                                                            keep='first')
    return data

def categorize_products(text):
    if not isinstance(text, str):
            return None

    # Clean text: convert to lowercase and extract words
    # Using simple split or string cleanup
    text= unidecode(text).lower().replace(',', '').replace('.', '')

    match = re.search(pattern, text.lower())
    if match:
        return classification_dict[match.group(1)]

    return None  # Or 'Uncategorized'

def categorize_store_brand(text):
    if not isinstance(text, str):
            return None

    # Clean text: convert to lowercase and extract words
    # Using simple split or string cleanup
    text= unidecode(text).lower().replace(',', '').replace('.', '')

    match = re.search(pattern2, text.lower())
    if match:
        return 1

    return 0  # Or 'Uncategorized'

def getLinks(url, pages, product_data):
    try:
        html = urlopen(url)
    except URLError:
        print(f"the url {url} had some problem so we skipping")
        return
    bs=BeautifulSoup(html.read(), 'html.parser')
    for child in bs.find(id="store.menu").children:
        # Check if the child is an HTML tag (and not just blank whitespace text)
        if child.name is not None:
            for link in child.find_all('a'):
                if link.attrs.get('href') not in pages:
                    product_list = bs.find_all('div', {'class':'product details product-item-details'})
                    for product in product_list:
                        one_product = []
                        one_product.append(link.attrs.get('href'))
                        one_product.append(product.find(attrs={"data-product-id":True}).attrs['data-product-id'])
                        one_product.append(product.find(class_="product name product-item-name").get_text())
                        one_product.append(product.find("span", class_="price-wrapper").attrs['data-price-amount'])
                        try:
                            one_product.append(product.find(attrs={"data-product-sku":True}).attrs['data-product-sku'])
                        except AttributeError:
                            one_product.append("")
                        print(one_product)
                        product_data.append(one_product)
                    newPage = link.attrs.get('href')
                    print(newPage)
                    pages.add(newPage)
                    getLinks(newPage, pages, product_data)

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
