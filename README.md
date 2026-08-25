# ✈️ Multi-Cloud Real-Time Flight Data Pipeline & CDC Analytics Engine

A multi-cloud data engineering capstone project that orchestrates real-time global flight telemetry ingestion from the OpenSky Network API, stores raw JSON payloads in AWS S3, cleans and standardizes nested spatial metrics using PySpark into Delta Lake format, and automates CDC (Change Data Capture) analytics loading into Snowflake using Storage Integration, Streams, and Tasks.

---

## 🏗️ End-to-End Architecture

```text
┌─────────────────────────┐
│   OpenSky Network API   │  (Live Global Aircraft Telemetry)
└────────────┬────────────┘
             │ (HTTP REST Ingestion)
             ▼
┌─────────────────────────┐
│   Apache Airflow DAG    │  --> (multicloud_flight_ingestion_boto3)
└────────────┬────────────┘
             │ (Raw JSON Stream via Boto3)
             ▼
┌─────────────────────────┐
│    AWS S3 Raw Zone      │  --> (s3://capstone1010/raw/)
└────────────┬────────────┘
             │ (s3a Protocol / PySpark Processing)
             ▼
┌─────────────────────────┐
│   PySpark Data Engine   │  --> (Unnest Matrix Array, Schema Casting & Delta Write)
└────────────┬────────────┘
             │ (Parquet / Delta Format)
             ▼
┌─────────────────────────┐
│  AWS S3 Processed Zone  │  --> (s3://capstone1010/processed/flight_delta_table/)
└────────────┬────────────┘
             │ (AWS IAM Role-Based Storage Integration)
             ▼
┌─────────────────────────┐
│  Snowflake Landing Zone │  --> (FLIGHT_RAW_LANDING Table via COPY INTO)
└────────────┬────────────┘
             │ (Stream CDC Trigger & QUALIFY Deduplication)
             ▼
┌─────────────────────────┐
│ Snowflake Target Zone   │  --> (FLIGHT_ANALYTICS_TARGET - Real-Time Merge Table)
└─────────────────────────┘
