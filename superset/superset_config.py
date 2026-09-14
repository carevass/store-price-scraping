import os
from env_vars import PG_HOST, PG_USER, PG_PASSWORD, PG_DATABASE, PG_PORT


# PostgreSQL metadata store connection string
SQLALCHEMY_DATABASE_URI = f'postgresql+psycopg2://{PG_USER}:{PG_PASSWORD}@{PG_HOST}:{PG_PORT}/superset_metadata'
