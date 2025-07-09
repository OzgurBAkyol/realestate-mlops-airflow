<p align="center">
  <img src="https://upload.wikimedia.org/wikipedia/commons/thumb/7/71/AirflowLogo.svg/500px-AirflowLogo.svg.png" width="140"/>
  &nbsp;&nbsp;&nbsp;&nbsp;
  <img src="https://sourcebae.com/blog/wp-content/uploads/2023/08/1_b_al7C5p26tbZG4sy-CWqw.png" height="90"/>
  &nbsp;&nbsp;&nbsp;&nbsp;
  <img src="https://miro.medium.com/v2/resize:fit:802/format:webp/0*pxlnDm-ncQdC0UEL.png" height="90"/>a
</p>

<h1 align="center">🏡 Real Estate ML Pipeline with Airflow & AWS</h1>

<p align="center">
  <b>End-to-end automated ETL and Machine Learning pipeline using Airflow, AWS S3, and Python.</b>
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
flowchart TD
    A[Extract Data] --> B[Clean & Transform]
    B --> C[Feature Engineering]
    C --> D[Train ML Model]
    D --> E[Predict and Save]

    subgraph Extract
        A_note[Fetch property data from Zillow API]
    end
    subgraph Clean
        B_note[Remove nulls, standardize formats]
    end
    subgraph Feature
        C_note[One-hot encoding and custom feature creation]
    end
    subgraph Train
        D_note[Train a RandomForest model, evaluate performance]
    end
    subgraph Predict
        E_note[Make predictions and write results to S3]
    end

    A --> A_note
    B --> B_note
    C --> C_note
    D --> D_note
    E --> E_note
