from dotenv import load_dotenv
load_dotenv()
import os

PG_HOST = os.getenv("PG_HOST")
PG_USER = os.getenv("PG_USER")
PG_PASSWORD = os.getenv("PG_PASSWORD")
PG_DATABASE = os.getenv("PG_DATABASE")
PG_PORT = os.getenv("PG_PORT")


STORE1_STARTLINK = os.getenv("STORE1_STARTLINK")
STORE2_STARTLINK = os.getenv("STORE2_STARTLINK")
