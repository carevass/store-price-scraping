CREATE TABLE IF NOT EXISTS store1(scraped_site text, scrape_datetime timestamp, product_id text,
product_name text,price float, product_sku text);
ALTER TABLE store1
    SET SCHEMA rawdata;


CREATE TABLE IF NOT EXISTS store2(scrape_datetime timestamp,
  product_id text, product_name text, description text, mpn text,
  sku text, brand_name text, lowPrice float, highPrice float, price float,
  offer_availability text, product_sku text, offer_priceValidUntil timestamp);
ALTER TABLE store2
    SET SCHEMA rawdata;
