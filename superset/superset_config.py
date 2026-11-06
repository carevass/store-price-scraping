import os
from env_vars import PG_HOST, PG_USER, PG_PASSWORD, PG_DATABASE, PG_PORT


# PostgreSQL metadata store connection string
SQLALCHEMY_DATABASE_URI = f'postgresql+psycopg2://{PG_USER}:{PG_PASSWORD}@{PG_HOST}:{PG_PORT}/superset_metadata'
SQL_MAX_ROW = 10000000
DISPLAY_MAX_ROW = 100000000  # Adjust this value as needed
FEATURE_FLAGS =  {
  "EMBEDDED_SUPERSET": True, # requirement
  "GUEST_ROLE_NAME": "Public", # you might need to edit role permissions when 403 error
  "GUEST_TOKEN_JWT_EXP_SECONDS": 300  # 5 minutes, or you could set it longer
}
