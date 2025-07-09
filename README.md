<p align="center">
  <img src="https://airflow.apache.org/images/airflow_logo.png" width="100"/>
  &nbsp;&nbsp;&nbsp;
  <img src="https://a0.awsstatic.com/libra-css/images/logos/aws_logo_smile_1200x630.png" height="60"/>
  &nbsp;&nbsp;&nbsp;
  <img src="https://upload.wikimedia.org/wikipedia/commons/0/05/Scikit_learn_logo_small.svg" height="60"/>
  &nbsp;&nbsp;&nbsp;
  <img src="https://miro.medium.com/v2/resize:fit:802/format:webp/0*pxlnDm-ncQdC0UEL.png" height="60"/>
</p>

<h1 align="center">🏡 Real Estate ML Pipeline with Airflow & AWS</h1>

<p align="center">
  <b>End-to-end automated ETL + ML pipeline for real estate price prediction using Airflow, AWS S3, and scikit-learn.</b>
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
