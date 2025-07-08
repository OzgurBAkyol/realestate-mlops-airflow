import pandas as pd
import boto3
import json
from io import BytesIO
from datetime import datetime

bucket_name = "myawsbucketetlpipebucket"
raw_folder = "raw"
cleaned_folder = "cleaned"

s3 = boto3.client("s3")

def get_latest_raw_file():
    response = s3.list_objects_v2(Bucket=bucket_name, Prefix=raw_folder)
    files = [obj["Key"] for obj in response.get("Contents", []) if obj["Key"].endswith(".json")]
    if not files:
        raise Exception("No JSON files found in raw folder.")
    latest_file = max(files, key=lambda x: s3.head_object(Bucket=bucket_name, Key=x)["LastModified"])
    return latest_file

def read_json_from_s3(key):
    response = s3.get_object(Bucket=bucket_name, Key=key)
    content = response["Body"].read().decode("utf-8")
    data = json.loads(content)
    
    try:
        listings = data["results"]
        return pd.json_normalize(listings)
    except KeyError as e:
        print(f"Hata: Beklenen anahtar bulunamadı: {e}")
        print(f"Data'nın ilk seviyesi: {list(data.keys())}")
        raise

def clean_df(df):
    columns_to_keep = ["bathrooms", "bedrooms", "city", "homeStatus", "homeType", "livingArea", "price", "rentZestimate", "zipcode"]
    return df[[col for col in columns_to_keep if col in df.columns]]

def write_csv_to_s3(df, key):
    csv_buffer = BytesIO()
    df.to_csv(csv_buffer, index=False)
    s3.put_object(Bucket=bucket_name, Key=key, Body=csv_buffer.getvalue())
    print(f"{key} klasörüne başarıyla yazıldı.")

def main():
    latest_key = get_latest_raw_file()
    print(f"En son dosya: {latest_key}")
    df = read_json_from_s3(latest_key)
    cleaned_df = clean_df(df)
    
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    cleaned_key = f"{cleaned_folder}/zillow_cleaned_{timestamp}.csv"
    write_csv_to_s3(cleaned_df, cleaned_key)

if __name__ == "__main__":
    main()