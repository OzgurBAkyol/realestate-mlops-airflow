from airflow import DAG
from airflow.operators.python import PythonOperator
from datetime import datetime, timedelta
import sys
import os

# 👇 Script yolunu ekle
sys.path.append(os.path.join(os.environ['HOME'], 'airflow/dags/zillow_transform'))

# 👇 Feature engineering fonksiyonunu import et
from zillow_feature_engineer import main as feature_main

default_args = {
    'owner': 'airflow',
    'start_date': datetime(2025, 7, 8),
    'retries': 2,
    'retry_delay': timedelta(minutes=1)
}

with DAG(
    dag_id='zillow_feature_engineering',
    default_args=default_args,
    schedule_interval=None,
    catchup=False
) as dag:

    feature_task = PythonOperator(
        task_id='run_feature_engineering',
        python_callable=feature_main
    )