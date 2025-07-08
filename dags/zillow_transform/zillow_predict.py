import pandas as pd
import boto3
import joblib
import json
from io import BytesIO
from datetime import datetime
import os

bucket_name = "myawsbucketetlpipebucket"
features_folder = "features"
models_folder = "models"
predictions_folder = "predictions"

s3 = boto3.client("s3")

def get_latest_file(folder, extension):
    response = s3.list_objects_v2(Bucket=bucket_name, Prefix=folder)
    files = [obj["Key"] for obj in response.get("Contents", []) if obj["Key"].endswith(extension)]
    if not files:
        raise Exception(f"No {extension} files found in {folder} folder.")
    latest_file = max(files, key=lambda x: s3.head_object(Bucket=bucket_name, Key=x)["LastModified"])
    return latest_file

def read_csv_from_s3(key):
    obj = s3.get_object(Bucket=bucket_name, Key=key)
    return pd.read_csv(obj["Body"])

def load_model_from_s3(key):
    obj = s3.get_object(Bucket=bucket_name, Key=key)
    return joblib.load(BytesIO(obj["Body"].read()))

def write_csv_to_s3(df, key):
    buffer = BytesIO()
    df.to_csv(buffer, index=False)
    s3.put_object(Bucket=bucket_name, Key=key, Body=buffer.getvalue())
    print(f"{key} klasörüne tahmin sonuçları yazıldı.")

def main():
    feature_key = get_latest_file(features_folder, ".csv")
    model_key = get_latest_file(models_folder, ".joblib")   
    
    print(f"Feature dosyası: {feature_key}")
    print(f"Model dosyası: {model_key}")

    df = read_csv_from_s3(feature_key)
    model = load_model_from_s3(model_key)

    # Modelin beklediği sütunları al
    X_raw = df.drop(columns=["price"], errors="ignore")
    X_encoded = pd.get_dummies(X_raw)

    # Eksik sütunları modelin eğitildiği sütunlarla tamamla
    expected_features = model.feature_names_in_
    for col in expected_features:
        if col not in X_encoded.columns:
            X_encoded[col] = 0  # eksik olanlar 0 ile doldurulur
    X_encoded = X_encoded[expected_features]  # sıralamayı eşitle

    predictions = model.predict(X_encoded)
    df["predicted_price"] = predictions

    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    prediction_key = f"{predictions_folder}/zillow_predictions_{timestamp}.csv"
    write_csv_to_s3(df, prediction_key)

if __name__ == "__main__":
    main()