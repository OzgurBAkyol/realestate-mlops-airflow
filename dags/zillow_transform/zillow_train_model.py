import pandas as pd
import numpy as np
import boto3
import joblib
import os
from io import BytesIO
from datetime import datetime
from sklearn.ensemble import RandomForestRegressor
from sklearn.model_selection import train_test_split
from sklearn.metrics import mean_absolute_error
from sklearn.metrics import mean_squared_error

# S3 ayarları
bucket_name = "myawsbucketetlpipebucket"
features_folder = "features"
models_folder = "models"

# S3 bağlantısı
s3 = boto3.client("s3")

def get_latest_features_file():
    response = s3.list_objects_v2(Bucket=bucket_name, Prefix=features_folder)
    files = [obj["Key"] for obj in response.get("Contents", []) if obj["Key"].endswith(".csv")]
    if not files:
        raise Exception("No feature files found.")
    latest_file = max(files, key=lambda x: s3.head_object(Bucket=bucket_name, Key=x)["LastModified"])
    return latest_file

def load_features_from_s3(key):
    response = s3.get_object(Bucket=bucket_name, Key=key)
    df = pd.read_csv(BytesIO(response["Body"].read()))
    return df

def train_and_save_model(df):
    target = "price"
    X = df.drop(columns=[target])
    y = df[target]

    # Kategorik sütunları sayısala çevir
    X = pd.get_dummies(X)

    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

    model = RandomForestRegressor(n_estimators=100, random_state=42)
    model.fit(X_train, y_train)

    predictions = model.predict(X_test)
    mse = mean_squared_error(y_test, predictions)
    rmse = np.sqrt(mse)
    print(f"RMSE: {rmse:.2f}")

    # Save model to S3
    buffer = BytesIO()
    joblib.dump(model, buffer)
    buffer.seek(0)

    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    model_key = f"models/zillow_model_{timestamp}.joblib"
    s3.put_object(Bucket=bucket_name, Key=model_key, Body=buffer.getvalue())
    print(f"{model_key} model klasörüne yüklendi.")

def main():
    latest_key = get_latest_features_file()
    print(f"En son feature dosyası: {latest_key}")
    df = load_features_from_s3(latest_key)
    train_and_save_model(df)

if __name__ == "__main__":
    main()