# ✈️ Multi-Cloud Flight Data Pipeline (Medallion Architecture)

A multi-cloud data engineering pipeline that ingests, cleans, and analyzes live global flight telemetry using a **Medallion Architecture** pattern (Bronze $\rightarrow$ Silver $\rightarrow$ Gold) across Apache Airflow, AWS S3, Databricks PySpark, and Snowflake.

---

## 🏗️ Medallion Architecture & Data Flow

```text
┌─────────────────────────┐
│   OpenSky Network API   │  (Live Global Aircraft Telemetry)
└────────────┬────────────┘
             │ (HTTP REST / Boto3 Streaming)
             ▼
┌─────────────────────────┐
│     BRONZE LAYER        │  AWS S3 Raw Zone
│ (Raw JSON Payloads)     │  s3://capstone1010/raw/
└────────────┬────────────┘
             │ (s3a Protocol / Array Explode & Schema Normalization)
             ▼
┌─────────────────────────┐
│     SILVER LAYER        │  Databricks PySpark & Delta Lake
│ (Cleaned & Structured)  │  s3://capstone1010/processed/flight_delta_table/
└────────────┬────────────┘
             │ (AWS IAM Storage Integration / COPY INTO & Streams)
             ▼
┌─────────────────────────┐
│      GOLD LAYER         │  Snowflake Analytics & CDC Target
│ (Deduplicated CDC Sink) │  FLIGHT_ANALYTICS_TARGET (Real-Time Upsert Sink)
└─────────────────────────┘

## 🛠️ Tech Stack

* **Ingestion & Orchestration:** Apache Airflow (PyCharm / Boto3) ➔ AWS S3 (Raw JSON)
* **Processing Engine:** Databricks PySpark ➔ AWS S3 (Delta Lake Storage)
* **Warehouse & CDC Analytics:** Snowflake (Storage Integration ➔ Streams & Tasks)

---
