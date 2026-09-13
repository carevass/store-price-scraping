"""
01. Supermarket data project - cleaning & transformaion

Date created: 19 August 2026
Last updated: 19 August 2026

author: Carlos Restituyo 


This takes in raw data scraped from supermarket websites on products, cleans and tranforms
the data into tables to be exported back to Postgres to be used in making dashboards. 

"""

#%% Preliminaries
#%%% Packages
import pandas as pd
import hashlib
from sqlalchemy import create_engine, text
import re
from unidecode import unidecode
from env_vars import PG_HOST, PG_USER, PG_PASSWORD, PG_DATABASE, PG_PORT

#import numpy as np

#%%% Connections
conn_string = f'postgresql+psycopg://{PG_USER}:{PG_PASSWORD}@{PG_HOST}:{PG_PORT}/{PG_DATABASE}'
db = create_engine(conn_string)
#%%% Functions
def get_hash(text):
    hash_object = hashlib.md5(text.encode())
    return hash_object.hexdigest()
def clean_data(df):
    data = pd.read_sql_query(f'SELECT * FROM rawdata.{df}', db)
    data['supermarket_name'] = f'{df}'
    data['supermarket_id'] = data['supermarket_name'].map(store_dict)

    #2. hash product names
    data['product_name_id'] = data['product_name'] + data['product_id']
    data['hashed_product'] = data['product_name_id'].apply(get_hash)
    if df == 'nacional':
        #special cleaning for nacional, we added scraped site after starting scraping so we are backfilling these values for the same products as before
        
        group_cols = ["hashed_product"]          
        data["scraped_site"] = (
            data.groupby(group_cols)["scraped_site"].bfill()
        )
         
        #data["product_sku"] = data["product_sku"].replace("", np.nan)
        #data["product_sku"] = (
        #    data.groupby(group_cols)["product_sku"].bfill().ffill()
        #)
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
#%%% Dicionaries
store_dict = {
    "store1":"store 1", #random numbers to use as ID
    "store2":"store 2",
    }

classification_dict = {
    

    "habichuelas":"beans",
    "habichuela":"beans", # work on accepting plural and singular variants in pattern
    "habas":"beans",
    "maiz":"beans",   
    "garbanzos":"beans",
    "habas":"beans",
    "chicharos":"beans",

    "cerveza":"beer",         
    "hard seltzer":"beer",
    "smirnoff":"beer",
    "four loko":"beer",
    "roskoff":"beer",

    
    

    "pan":"bread",     
    "bagel":"bread",
    "tostadas":"bread",
    "croissants":"bread",               
    
    "cafe":"coffee",


    "salsa":"condiments",               
    "caldo":"condiments",               
    "sazon":"condiments",               
    "azucar":"condiments",               
    "miel":"condiments",               
    "paprika":"condiments",               
    "crema inglesa":"condiments",               
    "crema agria":"condiments",               
    "mostaza":"condiments",               
    "sazonador":"condiments",
    "splenda":"condiments",               
    "sirop":"condiments",               
    "stevia":"condiments",               
    "pimientos":"condiments",
    "edulcorante":"condiments",
    "endulzante":"condiments",

               
    "sal":"salt",               
      
    "aceite":"cooking oil",               

    "vaso":"cookware",               
    "tapa":"cookware",               
    "servilleta":"cookware",               
    "sarten":"cookware",               
    "molde":"cookware",               
    "contenedor":"cookware",               
    "plato":"cookware",     
    "platos":"cookware",     
    "cuberteria":"cookware",     
    "botella":"cookware",               
    "cortador de galletas":"cookware",               
    "cafetera":"cookware",  
    "capacillos":"cookware",     


    "huevos":"eggs",     

    "mango":"fruits",     
    "melocoton":"fruits",     
    "compota":"fruits",     
    "manzana":"fruits",     
    "pina":"fruits",     
    "auyama":"fruits",     
    "lychees":"fruits",     
    "frutas":"fruits",     
    "moras":"fruits",     
    "datiles":"fruits",     
    "chinola":"fruits",     
    "peras":"fruits",     
    "clementinas":"fruits",     
    "mapuey":"fruits",     
    "naranja":"fruits",     
    "guineo":"fruits",     
    "platano":"fruits",     
    "melon":"fruits",     
    "uva":"fruits",     
    "guineitos":"fruits",     

    "bombillo":"house care",     
    "limpiador":"house care",     
    "suavizante":"house care",     
    "detergente":"house care",     
    "papel":"house care",     
    "removedor":"house care",     
    "ambientador":"house care",     
    "pila":"house care",     
    "velon":"house care",     
    "lejia":"house care",     
    "desengrasante":"house care",     
    "cera":"house care",     
    "esponja":"house care",     
    "escoba":"house care",     
    "moho":"house care",     
    "cloro":"house care",     
    "encendedor":"house care",     
    "endendedores":"house care",     
    "betun":"house care",     
    "ratones":"house care",     
    "inodoro":"house care",     
    "scapuntas":"house care",     
    "insecticida":"house care",     
    "vela":"house care",     
    "quitamanchas":"house care",
    "desinfectante":"house care",
    "lavaplatos":"house care",
    "guantes":"house care",
    "difusor":"house care",
    "deshumidificador":"house care",
    "ambiental":"house care",
    "suaper":"house care",
    "almidon":"house care",
    "funda":"house care",
    "fundas":"house care",
    "madera":"house care",
    "bicarbonato":"house care",
    "fregador":"house care",
    "esponjillas":"house care",
    "pano":"house care",
    "panito":"house care",
    "muebles":"house care",
    "carbosota":"house care",
    "baking soda":"house care",



    "jugo":"juice",     
    "zumo":"juice",     

    "bebida hidratante":"energy drink",
    "bebida electrolito":"energy drink",
    "gatorade":"energy drink",
    "bebida para hidratacion":"energy drink",


    "leche de almendra":"milk substitute",    
    "leche de soya":"milk substitute", 
    "leche de avena":"milk substitute",
    "leche de pistacho":"milk substitute",    
    
    "mantequilla de avena":"milk substitute",    
    "mantequilla de almendra":"milk substitute",    
    "mantequilla de cajuil":"milk substitute",    
    "margarina":"milk substitute",



    "leche":"milk",
    "carnation":"milk",
    "cocoa":"milk",
    "formula":"milk",
    "bebida nutricional":"milk",
    "suplemento":"milk",


    "mantequilla":"butter",
    
    "yogurt":"yoghurt",


    "tortellini":"pasta",
    "tortelloni":"pasta",
    "lasagna":"pasta",
    "linguine":"pasta",
    "gnocchi":"pasta",
    "antipasto":"pasta",
    "ravioli":"pasta",
    "lasagna":"pasta",
    "macarrones":"pasta",
    "spaghetti":"pasta",
    "spaghettoni":"pasta",
    "raviolini":"pasta",
    "pasta rellena":"pasta",

    "plantilla":"personal care",
    "higienico":"personal care",
    "toallas":"personal care",
    "toallitas":"personal care",
    "tampones":"personal care",
    "jabon":"personal care",
    "exfoliante":"personal care",
    "wipes":"personal care",
    "enjuague":"personal care",
    "manitas":"personal care",
    "desodorante":"personal care",
    "tinte":"personal care",
    "cepillo":"personal care",
    "rizador":"personal care",
    "humectante":"personal care",
    "mascarilla":"personal care",
    "shampoo":"personal care",
    "acondicionador":"personal care",
    "dental":"personal care",
    "protectores":"personal care",
    "rasuradora":"personal care",
    "panales":"personal care",
    "facial":"personal care",
    "capilo":"personal care",
    "teals":"personal care",
    "spf":"personal care",
    "serum":"personal care",
    "dental":"personal care",
    "repelente":"personal care",
    "pastillas":"personal care",
    "absorbente":"personal care",
    "desmanchador":"personal care",


    "gato":"pet care",
    "perro":"pet care",
    "pez":"pet care",
    "mascota":"pet care",
    "mascotas":"pet care",
    
    "harina":"processed grain",
    "tortitas":"processed grain",
    "tortillas":"processed grain",
    "pancakes":"processed grain",
    "avena":"processed grain",
    "cereal":"processed grain",
    "tortilla":"processed grain",
    "casabe":"processed grain",
    "waffles":"processed grain",
    "papilla":"processed grain",
    "masa":"processed grain",
    "granola":"processed grain",
    "barra":"processed grain",



    "hummus":"prepared foods",
    "pizza":"prepared foods",
    "empanada":"prepared foods",
    "empanadas":"prepared foods",
    "empanaditas":"prepared foods",
    "pastel en hoja":"prepared foods",
    "catibias":"prepared foods",


    "barra de chocolate":"chocolate",





    
    "salami":"processed meat",
    "salchicha":"processed meat",
    "jamon":"processed meat",
    "prosciutto":"processed meat",
    "mortadella":"processed meat",
    "nuggets":"processed meat",
    "tapas":"processed meat",
    "charcuteria":"processed meat",

    "arroz":"grain",
    "trigo":"grain",
    "farro":"grain",
    "quinoa":"grain",

    "gelatina":"snacks",
    "snack":"snacks",
    "galletas":"snacks",
    "galletitas":"snacks",
    "dulce de":"snacks",
    "chips":"snacks",
    "pipas":"snacks",
    "platanitos":"snacks",
    "yuquitas":"snacks",
    "palitos":"snacks",
    "galleta":"snacks",
    "tiras":"snacks",
    "palito":"snacks",
    "caramelos":"snacks",
    "chicharron":"snacks",
    "chispas":"snacks",
    "donas":"snacks",
    "aros de cebolla":"snacks",
    "marshmallow":"snacks",
    "pudding":"snacks",
    "fritas":"snacks",
    "palomitas":"snacks",
    "fun size":"snacks",
    "bombon":"snacks",
    "bombones":"snacks",
    "hershey":"snacks",
    "haribo":"snacks",
    "m&m's":"snacks",
    "choco trio":"snacks",
    "paletas":"snacks",
    "pretzel":"snacks",
    "dip":"snacks",

    "pastel":"cake",
    "bizcocho":"cake",
    "boquilla":"cake",
    "extracto":"cake",
    "coco rallado":"cake",
    "budin":"cake",
    "relleno para pie":"cake",
    "levadura":"cake",
    "pudin":"cake",
    "hornear":"cake",
    "vainilla":"cake",


    "cordero":"fresh meat",
    "carne":"fresh meat",
    "pechuga":"fresh meat",
    "churrasco":"fresh meat",
    "palomilla":"fresh meat",
    "secreto":"fresh meat",
    "steak":"fresh meat",
    "costilla":"fresh meat",
    "hamburguesa":"fresh meat",
    "pavo entero":"fresh meat",
    "pavo congelado":"fresh meat",
    "muslo":"fresh meat",
    "pico y pala":"fresh meat",
    "pollo entero":"fresh meat",
    "gallina congelada":"fresh meat",
    "tocineta":"fresh meat",
    "alas":"fresh meat",
    
    "queso":"cheese",
    "auricchio":"cheese",
    "creme fraiche":"cheese",

    "refresco":"soft drinks",
    "agua tonica":"soft drinks",
    "agua gasificada":"soft drinks",
    "agua mineral":"soft drinks",
    "malta":"soft drinks",
    "agua tonica":"soft drinks",
    "tonica":"soft drinks",
    "club soda":"soft drinks",
    "agua tonica":"soft drinks",

    "agua":"water",
    
    "te":"tea",
    
    "batata":"vegetables",   
    "yautia":"vegetables",    
    "zanahoria":"vegetables",
    
    "papa":"vegetables",
    "aji":"vegetables",
    "tofu":"vegetables",
    "berenjena":"vegetables",
    "tomates":"vegetables",
    "remolacha":"vegetables",
    "trufas":"vegetables",
    "vegetales mixtos":"vegetables",
    "alcachofa":"vegetables",
    "ajo":"vegetables",
    "rucula":"vegetables",
    "apio":"vegetables",
    "name":"vegetables",
    "cebolla":"vegetables",
    "pepino":"vegetables",
    "tofu":"vegetables",

    "vino":"wine",
    "vinos":"wine",
    "oporto":"wine",
    "sidra":"wine",
    "champin":"wine",
    "cava":"wine",
    "prosecco":"wine",
    "espumante":"wine",
    "jerez":"wine",



    "aguardiente":"spirits",
    "cognac":"spirits",
    "brandy":"spirits",
    "ron":"spirits",
    "aperitivo":"spirits",
    "cachaca":"spirits",
    "grappa":"spirits",
    "ginebra":"spirits",
    "licor":"spirits",
    "sangria":"spirits",
    "coctel":"spirits",
    "tequila":"spirits",
    "mezcla":"spirits",
    "vodka":"spirits",
    "mamajuana":"spirits",
    "whisky":"spirits",
    "bitter":"spirits",
    "mezcal":"spirits",
    "mojito":"spirits",
    "daiquiri":"spirits",
    "ponche":"spirits",


    }
# 1. Sort keys by length (descending) so longer terms take priority (e.g., "goat milk" before "milk")
#sorted_keys = sorted(classification_dict.keys(), key=len, reverse=True)

# 2. Build regex pattern with word boundaries (\b)
pattern = r'\b(' + '|'.join(map(re.escape, classification_dict)) + r')\b'

#%%Load data

#eventually have this iterate over a list of tables
'''
nacional = pd.read_sql_query('SELECT * FROM rawdata.nacional', db)
sirena = pd.read_sql_query('SELECT * FROM rawdata.sirena', db)


#%%Data manipulation

nacional['supermarket_name'] = 'nacional'
sirena['supermarket_name'] = 'sirena'

#1. remove same-day duplicates, leave only one product per day in the data set
#there may be multiple entries per day because of debugging so this ensures
#we have at most one product entry per day
nacional['scrape_date'] = pd.to_datetime(nacional['scrape_datetime']).dt.date


#use all columns except price to consider duplicates
nacional = nacional.sort_values('scrape_datetime').drop_duplicates(subset=nacional.columns.difference(['price','scrape_datetime']), 
                                                        keep='first')

#2. hash product names


nacional['hashed_product'] = nacional['product_name'].apply(get_hash)
'''
store1 = clean_data('store1')

store2 = clean_data('store2')

# append data
sm_data = pd.concat([store1,store2], ignore_index = True)

sm_data['category'] = sm_data['product_name'].apply(categorize_products) 

#sm_data[['product_name']].sample(n = 1000, random_state = 541557).to_csv('proc/training_data.csv', index = False)

#this x must be 0 eventually
x =sm_data[sm_data.category.isna()][['product_name', 'category']]



#%% Export data
#prepare the queries to create the tables we will use
 

with db.begin() as conn:
    # Wrap your string with text()
    store_table = text('CREATE TABLE IF NOT EXISTS proc.store_info(supermarket_id text primary key, supermarket_name text)')
    product_table = text('CREATE TABLE IF NOT EXISTS proc.product_info(supermarket_id text, hashed_product text primary key, product_name text, category text)')
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
                                                      'product_name', 'category']].to_sql('product_info', db, if_exists= 'delete_rows',index=False, schema = 'proc')



