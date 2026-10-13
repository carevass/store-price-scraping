import pendulum
from airflow.providers.standard.operators.bash import BashOperator
from airflow.providers.standard.operators.python import PythonOperator
from airflow.providers.http.operators.http import HttpOperator
from airflow.sdk import DAG

with DAG(
dag_id="01_extract_transform",
start_date=pendulum.today('UTC').add(days=-14),
schedule="0 15 */3 * *",
):

    extract_store1 = HttpOperator(
        task_id="extract_store1",
        endpoint="/extract_store1",
        method="POST",
        http_conn_id="scraping_container",

        )

    extract_store2 = HttpOperator(
        task_id="extract_store2",
        endpoint="/extract_store2",
        method="POST",
        http_conn_id="scraping_container",

        )
    
    extract_store3 = HttpOperator(
        task_id="extract_store3",
        endpoint="/extract_store3",
        method="POST",
        http_conn_id="scraping_container",

        )

    transform_data = HttpOperator(
        task_id="transform_data",
        endpoint="/transform",
        method="POST",
        http_conn_id="scraping_container",

        )


[extract_store1, extract_store2, extract_store3] >> transform_data
