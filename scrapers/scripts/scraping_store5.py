import requests
import pandas as pd
from sqlalchemy import create_engine, text
import datetime
from scripts.env_vars import PG_HOST, PG_USER, PG_PASSWORD, PG_DATABASE, PG_PORT, STORE5_STARTLINK, STORE5_AUTH
from bs4 import BeautifulSoup
import time

def main():
    base_url = STORE5_STARTLINK


    categories = list(range(1,31)) + [204, 341, 342, 343]

    params = {
        "categoryId":0,
        "pagenumber":1,
        "viewmode":"grid",
        "orderby":0,

        }

    headers = {
        "authority": STORE5_AUTH,
        "method":"GET",
        "scheme":"https",
        "Accept":"*/*",
        "Accept-language":"en-US,en;q=0.9,sv;q=0.8,es;q=0.7,fr;q=0.6",
        "Priority":"u=1;i",
        "Sec-Ch-Ua":'"Chromium";v="152", "Not?A_Brand";v="24", "Google Chrome";v="152"',
        "Sec-Ch-Ua-Platform":'"Windows"',
        "Sec-Fetch-Dest":"empty",
        "Sec-Fetch-Mode":"cors",
        "Sec-Fetch-Site":"same-origin",
        "User-Agent":"Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/152.0.0.0 Safari/537.36",
        "X-Requested-With":	"XMLHttpRequest",

            }
    product_data = []

    for cat in categories:
        params['categoryId'] = cat
        print(f"Category now {params['categoryId']}")
        params['pagenumber'] = 1
        for i in range(1,21):
            response = requests.get(base_url, params=params, headers = headers)
            #time.sleep(10)
            if response.status_code == 200:
                print(f"Going though page {params['pagenumber']}")
                bs=BeautifulSoup(response.text, 'html.parser')
                product_list = bs.find_all('div', {'class':'item-box'})
                #when out of bounds, do a length check on product_list if == 0 we can move on
                if len(product_list) > 0:
                    for product in product_list:
                        one_product = []
                        one_product.append(response.url)
                        one_product.append(product.find(attrs={"data-productid":True}).attrs['data-productid'])
                        one_product.append(product.find(class_="product-title").get_text())
                        one_product.append(product.find("span", class_="price actual-price").get_text())
                        one_product.append(product.find("a").get('href'))
                        product_data.append(one_product)
                else:
                    print("Finished section. Moving on...")
                    break
            else:
                print("Bad URL. Doing next section...")
                break
            params['pagenumber'] += 1
    titles=['scraped_site','product_id','product_name','price','product_sku']

    df = pd.DataFrame(product_data, columns= titles)
    df['scrape_datetime'] = datetime.datetime.now()
    df['price'] = df['price'].str.replace({'$':'',",":""})
    df['price_x'] = pd.to_numeric(df.price, errors="coerce")
    df['product_sku'] = df['product_sku'].str.replace('/Sku-', '')

    #export to postgresql database
    # establish connections
    conn_string = f'postgresql+psycopg://{PG_USER}:{PG_PASSWORD}@{PG_HOST}:{PG_PORT}/{PG_DATABASE}'
    db = create_engine(conn_string)

    with db.begin() as conn:

        store5_table = text('''CREATE TABLE IF NOT EXISTS rawdata.store5(scraped_site text,scrape_datetime timestamp, product_id text,
                            product_name text,price float, product_sku text);''')
        conn.execute(store5_table)


    df.to_sql('store5', db, if_exists= 'append', index=False, schema = 'rawdata')
