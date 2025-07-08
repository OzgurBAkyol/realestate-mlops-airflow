from airflow import DAG
from airflow.operators.python import PythonOperator
from datetime import datetime, timedelta
import subprocess

default_args = {
    'owner': 'airflow',
    'start_date': datetime(2025, 7, 8),
    'retries': 1,
    'retry_delay': timedelta(minutes=1),
}

def run_cleaning_script():
    subprocess.run(['python3', '/home/ubuntu/airflow/dags/zillow_transform/zillow_clean_and_save.py'], check=True)

with DAG(
    dag_id='zillow_clean_and_save_dag',
    default_args=default_args,
    schedule_interval='@daily',
    catchup=False
) as dag:

    clean_and_save = PythonOperator(
        task_id='run_cleaning_script',
        python_callable=run_cleaning_script
    )