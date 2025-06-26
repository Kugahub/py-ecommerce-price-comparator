from airflow import DAG
from airflow.operators.python import PythonOperator
from datetime import datetime
from scrapers.compare import compare_prices
from gdrive_uploader.upload_to_gdrive import upload_to_drive
import os

default_args = {
    "owner": "airflow",
    "start_date": datetime(2024, 1, 1),
}

with DAG("daily_scrape_compare_upload",
         default_args=default_args,
         schedule_interval="@daily",
         catchup=False) as dag:

    def wrapper_compare(**kwargs):
        search_query = kwargs["dag_run"].conf.get("search_query", "smart watch")
        print(f"[✔] Starting comparison for: {search_query}")
        output_path = compare_prices(search_query=search_query)
        kwargs['ti'].xcom_push(key='output_path', value=output_path)

    def wrapper_upload(**kwargs):
        ti = kwargs['ti']
        output_path = ti.xcom_pull(key='output_path')
        print(f"[✔] Starting upload for: {output_path}")
        upload_to_drive(output_path)

    scrape_task = PythonOperator(
        task_id="scrape_compare",
        python_callable=wrapper_compare,
        provide_context=True
    )

    upload_task = PythonOperator(
        task_id="upload_to_gdrive",
        python_callable=wrapper_upload,
        provide_context=True
    )
    scrape_task >> upload_task
