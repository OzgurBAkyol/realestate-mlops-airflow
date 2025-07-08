from airflow import DAG
from airflow.operators.python import PythonOperator
from airflow.operators.bash import BashOperator
from datetime import datetime, timedelta
import requests
import json
import boto3  # ✅ Lambda tetiklemek için gerekli

# 🔐 API Key ve host bilgisini ayrı bir JSON'dan okuyacağız (config_api.json)
with open('/home/ubuntu/airflow/config_api.json', 'r') as f:
    api_keys = json.load(f)

# 🔧 Default args
default_args = {
    'owner': 'airflow',
    'start_date': datetime(2025, 7, 8),
    'retries': 2,
    'retry_delay': timedelta(minutes=1),
}

# 🧪 Extract fonksiyonu
def extract_zillow_data(**kwargs):
    url = 'https://zillow56.p.rapidapi.com/search'
    headers = api_keys
    querystring = {
        "location": "Houston, TX",
        "output": "json",
        "status": "forSale",
        "sortSelection": "priorityscore",
        "listing_type": "by_agent",
        "doz": "any"
    }

    dt_now_string = datetime.now().strftime("%Y%m%d%H%M%S")
    output_file = f"/home/ubuntu/airflow/response_data_{dt_now_string}.json"

    response = requests.get(url, headers=headers, params=querystring)
    with open(output_file, "w") as f:
        json.dump(response.json(), f, indent=4)

    return output_file

# 🚀 Lambda fonksiyonunu tetikleyecek fonksiyon
def trigger_lambda_function():
    lambda_client = boto3.client('lambda', region_name='eu-north-1')
    response = lambda_client.invoke(
        FunctionName='zillow_raw_to_backup_copy',
        InvocationType='RequestResponse'
    )
    return response['StatusCode']

# 📦 DAG Tanımı
with DAG(
    dag_id='zillow_extract_to_s3',
    default_args=default_args,
    schedule_interval='@daily',
    catchup=False
) as dag:

    extract_data = PythonOperator(
        task_id='extract_zillow_data',
        python_callable=extract_zillow_data
    )

    upload_to_s3 = BashOperator(
        task_id='upload_json_to_s3',
        bash_command='aws s3 mv {{ ti.xcom_pull(task_ids="extract_zillow_data") }} s3://myawsbucketetlpipebucket/raw/',
    )

    trigger_lambda = PythonOperator(
        task_id='trigger_lambda_function',
        python_callable=trigger_lambda_function
    )

    extract_data >> upload_to_s3 >> trigger_lambda