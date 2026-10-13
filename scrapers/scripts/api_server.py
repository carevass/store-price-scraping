from fastapi import FastAPI

from scripts import scraping_store1, scraping_store2, scraping_store3, data_cleaning



app = FastAPI()


@app.post("/extract_store1")
def extract_store1():
    scraping_store1.main()

@app.post("/extract_store2")
def extract_store2():
    scraping_store2.main()

@app.post("/extract_store3")
def extract_store3():
    scraping_store3.main()

@app.post("/transform")
def transform():
    data_cleaning.main()
