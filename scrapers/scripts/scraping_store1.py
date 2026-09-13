from urllib.request import urlopen
from bs4 import BeautifulSoup
import pandas as pd
import random
from urllib.error import URLError
from sqlalchemy import create_engine, text
import datetime
from env_vars import PG_HOST, PG_USER, PG_PASSWORD, PG_DATABASE, PG_PORT, STORE1_STARTLINK


#collect data
pages=set()
product_data = []
random.seed(1234556)
def getLinks(url):
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
                    getLinks(newPage)
getLinks(STORE1_STARTLINK)


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
