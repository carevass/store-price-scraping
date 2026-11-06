import requests
import pandas as pd
from sqlalchemy import create_engine, text
import datetime
from scripts.env_vars import PG_HOST, PG_USER, PG_PASSWORD, PG_DATABASE, PG_PORT, STORE4_STARTLINK, STORE4_AUTH
from bs4 import BeautifulSoup
import time


def main():
    base_url = STORE4_STARTLINK
    sections = ['despensa', 'limpieza-y-desechables', 'mascotas', 'bebidas',
                'carnes-pescados-y-mariscos','cervezas-vinos-y-licores','frutas-y-vegetales',
                'panaderia-y-reposteria','platos-preparados','congelados','lacteos-y-huevos','quesos-y-embutidos']

    params = {
        "p":1,
        }

    headers = {
        "authority": STORE4_AUTH,
        "method":"GET",
        "scheme":"https",
        "Accept":"text/html, */*; q=0.01",
        "Accept-language":"en-US,en;q=0.9,sv;q=0.8,es;q=0.7,fr;q=0.6",
        "Cookie":"PHPSESSID=c13587fbe92d66d5bf0cd6b63306735a; sso_token=7fa99953743c9cb0422d184f0b67edff5b7453b5f395fc06654d046f12939dc8; form_key=4u5ql76NeDqsHgXB; mage-cache-storage={}; mage-cache-storage-section-invalidation={}; mage-cache-sessid=true; mage-messages=; form_key=4u5ql76NeDqsHgXB; X-Magento-Vary=d74abb1d2ef1f229b8d40b93613fb0b7ad0a3de5e61c1761b526dd7d1cee61d2; recently_viewed_product={}; recently_viewed_product_previous={}; recently_compared_product={}; recently_compared_product_previous={}; product_data_storage={}; section_data_ids={%22cart%22:1792081781%2C%22book_address_list%22:1792081781%2C%22customer_inventory%22:1792081780%2C%22shopping_list_section%22:1792081780}",
        "Priority":"u=1;i",
        "Host":STORE4_AUTH
        "Sec-Ch-Ua":'"Chromium";v="152", "Not?A_Brand";v="24", "Google Chrome";v="152"',
        "Sec-Fetch-Dest":"empty",
        "Sec-Fetch-Mode":"cors",
        "Sec-Fetch-Site":"same-origin",
        "TE":"trailers",
        "User-Agent":"Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/152.0.0.0 Safari/537.36",
        "X-Requested-With":	"XMLHttpRequest",

            }
    product_data = []
    for s in sections:
        #initialize navigation by defining first page per section and max amount of pages before going to the next section
        url = base_url + f'{s}'
        params['p'] = 1
        response = requests.get(url, params=params, headers = headers)
        bs=BeautifulSoup(response.text, 'html.parser')
        total_section_products = int(bs.find(class_="toolbar-number").get_text())
        max_pages = round(total_section_products/16)

        for page in range(1,max_pages+1):
            print(f"going through page {page}")
            response = requests.get(url, params=params, headers = headers)
            time.sleep(10)
            bs=BeautifulSoup(response.text, 'html.parser')

            product_list = bs.find_all('div', {'class':'product details product-item-details'})
            if product_list:
                for product in product_list:
                    one_product = []
                    one_product.append(response.url)
                    one_product.append(product.find(attrs={"data-product-id":True}).attrs['data-product-id'])
                    one_product.append(product.find(class_="product name product-item-name").get_text())
                    one_product.append(product.find("span", class_="price-wrapper").attrs['data-price-amount'])
                    if product.find(class_="stock unavailable"):
                        one_product.append('Out of Stock')
                    else:
                        one_product.append('In stock')
                    try:
                        one_product.append(product.find(attrs={"data-product-sku":True}).attrs['data-product-sku'])
                    except AttributeError:
                        print("problem getting the product sku")
                        one_product.append('')
                    print(one_product)
                    product_data.append(one_product)
            else:
                print(f"Section {s} finished.")
                continue

            params['p'] += 1
    titles=['scraped_site','product_id','product_name','price','availability','product_sku']

    df = pd.DataFrame(product_data, columns= titles)
    df['scrape_datetime'] = datetime.datetime.now()
    df['price'] =pd.to_numeric(df.price, errors="coerce")

    #export to postgresql database
    # establish connections
    conn_string = f'postgresql+psycopg://{PG_USER}:{PG_PASSWORD}@{PG_HOST}:{PG_PORT}/{PG_DATABASE}'
    db = create_engine(conn_string)

    with db.begin() as conn:

        store4_table = text('''CREATE TABLE IF NOT EXISTS rawdata.store4(scraped_site text,scrape_datetime timestamp, product_id text,
                            product_name text,price float, availability text, product_sku text);''')
        conn.execute(store4_table)


    df.to_sql('store4', db, if_exists= 'append', index=False, schema = 'rawdata')
