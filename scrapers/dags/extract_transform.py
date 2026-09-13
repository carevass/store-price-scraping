import pendulum
import requests
from airflow.providers.standard.operators.bash import BashOperator
from airflow.providers.standard.operators.python import PythonOperator
from airflow.sdk import DAG
from requests.exceptions import ConnectionError, MissingSchema



with DAG(
dag_id="01_extract_transform",
start_date=pendulum.today('UTC').add(days=-14),
schedule=None,
):
    
    extract_store1 = BashOperator(
        task_id="extract_store1",
        bash_command='docker exec supermarket_scraping python ./scripts/scraping_store1.py',
        )

    extract_store2 = BashOperator(
        task_id="extract_store2",
        bash_command='docker exec supermarket_scraping python ./scripts/scraping_store2.py',
        )
    
    transform_data = BashOperator(
        task_id="transform_data",
        bash_command='docker exec supermarket_scraping python ./scripts/data_cleaning.py',
        )
extract_store1 >> extract_store2 >> transform_data