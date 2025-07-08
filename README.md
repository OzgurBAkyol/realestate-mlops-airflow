# 🏡 Real Estate ML Pipeline with Airflow & AWS

<p align="center">
  <img src="https://raw.githubusercontent.com/apache/airflow/main/docs/apache-airflow/img/logos/airflow_horizontal_color.png" height="50" />
  &nbsp;&nbsp;&nbsp;&nbsp;
  <img src="https://a0.awsstatic.com/libra-css/images/logos/aws_logo_smile_1200x630.png" height="50" />
</p>

---

## 🚀 Overview
This project is a fully automated real estate ETL + ML pipeline using **Airflow**, **AWS S3**, **Python**, and **Scikit-learn**.

- Extracts property listings from Zillow API
- Stores raw & processed data to S3
- Trains a ML model to predict house prices
- Saves model and predictions to S3
- Orchestrated via Airflow DAG

---

## 🧱 Architecture

![Architecture](images/pipeline_architecture.png)

---

## 🧰 Tech Stack

- 🐍 Python
- ☁️ AWS S3
- 🧪 Pandas, Sklearn
- 🔁 Airflow (DAG orchestration)
- 💡 MLOps mindset

---

## 🔄 DAG Flow

```mermaid
graph TD;
    A[Extract Data] --> B[Clean & Transform];
    B --> C[Feature Engineering];
    C --> D[Train ML Model];
    D --> E[Predict and Save];
