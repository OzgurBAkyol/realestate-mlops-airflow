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

# 🧱 Python script'leri subprocess ile çalıştırılıyor
def run_extraction():
    subprocess.run(['python3', '/home/ubuntu/airflow/dags/zillow_extract.py'], check=True)

def run_cleaning():
    subprocess.run(['python3', '/home/ubuntu/airflow/dags/zillow_transform/zillow_clean_and_save.py'], check=True)

def run_feature_engineering():
    subprocess.run(['python3', '/home/ubuntu/airflow/dags/zillow_transform/zillow_feature_engineer.py'], check=True)

def run_model_training():
    subprocess.run(['python3', '/home/ubuntu/airflow/dags/zillow_transform/zillow_train_model.py'], check=True)

def run_prediction():
    subprocess.run(['python3', '/home/ubuntu/airflow/dags/zillow_transform/zillow_predict.py'], check=True)

# 🌀 DAG tanımı
with DAG(
    dag_id='zillow_full_etl_dag',
    default_args=default_args,
    schedule_interval='@daily',
    catchup=False
) as dag:

    extract_task = PythonOperator(
        task_id='extract_zillow_data',
        python_callable=run_extraction
    )

    clean_task = PythonOperator(
        task_id='clean_and_save_data',
        python_callable=run_cleaning
    )

    feature_task = PythonOperator(
        task_id='feature_engineering',
        python_callable=run_feature_engineering
    )

    train_task = PythonOperator(
        task_id='train_model',
        python_callable=run_model_training
    )

    predict_task = PythonOperator(
        task_id='predict_prices',
        python_callable=run_prediction
    )

    # 📈 Görev sırası
    extract_task >> clean_task >> feature_task >> train_task >> predict_task