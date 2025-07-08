import pandas as pd
import boto3
from io import BytesIO
from datetime import datetime

bucket_name = "myawsbucketetlpipebucket"
cleaned_folder = "cleaned"
features_folder = "features"

s3 = boto3.client("s3")

def get_latest_cleaned_file():
    response = s3.list_objects_v2(Bucket=bucket_name, Prefix=cleaned_folder)
    files = [obj["Key"] for obj in response.get("Contents", []) if obj["Key"].endswith(".csv")]
    if not files:
        raise Exception("No cleaned CSV files found.")
    latest_file = max(files, key=lambda x: s3.head_object(Bucket=bucket_name, Key=x)["LastModified"])
    return latest_file

def read_csv_from_s3(key):
    obj = s3.get_object(Bucket=bucket_name, Key=key)
    return pd.read_csv(BytesIO(obj["Body"].read()))

def feature_engineer(df):
    df["price_per_sqft"] = df["price"] / df["livingArea"]
    df["is_luxury"] = df["price"] > 1_000_000
    df["room_count"] = df["bedrooms"] + df["bathrooms"]
    df["zipcode_group"] = df["zipcode"].astype(str).str[:3]  # örn: 770xx
    return df

def write_features_to_s3(df, key):
    buffer = BytesIO()
    df.to_csv(buffer, index=False)
    s3.put_object(Bucket=bucket_name, Key=key, Body=buffer.getvalue())
    print(f"{key} klasörüne feature'lar yazıldı.")

def main():
    latest_key = get_latest_cleaned_file()
    print(f"En son temiz dosya: {latest_key}")
    df = read_csv_from_s3(latest_key)
    df_features = feature_engineer(df)
    
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    features_key = f"{features_folder}/zillow_features_{timestamp}.csv"
    write_features_to_s3(df_features, features_key)

if __name__ == "__main__":
    main()