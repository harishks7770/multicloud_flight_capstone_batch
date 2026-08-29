from datetime import datetime, timedelta, timezone
import json
import boto3
import requests
from airflow.decorators import dag, task
from airflow.hooks.base import BaseHook

default_args = {
    "owner": "multi_cloud_dev",
    "retries": 1,
    "retry_delay": timedelta(minutes=5),
}

@dag(
    dag_id="multicloud_flight_ingestion_boto3",
    default_args=default_args,
    schedule="@daily",  # Updated from schedule_interval
    start_date=datetime(2026, 1, 1),
    catchup=False,
    tags=["azure", "aws", "snowflake", "boto3"],
)
def pipeline():

    @task()
    def extract_and_upload_to_s3_boto3():
        # 1. Fetch raw data from OpenSky with explicit timeout
        url = "https://opensky-network.org/api/states/all"
        res = requests.get(url, timeout=30)
        
        if res.status_code != 200:
            raise ValueError(f"API call failed with status: {res.status_code}")

        raw_data = res.json()

        # 2. Recommended: Fetch AWS credentials dynamically from Airflow Connection
        # Alternatively, boto3 automatically picks up environment variables / IAM roles
        # if aws_access_key_id and aws_secret_access_key are omitted.
        
        # Example using hardcoded values safely fixed:
        s3_client = boto3.client(
            "s3",
            aws_access_key_id="YOUR_ACCESS_KEY_ID",
            aws_secret_access_key="YOUR_SECRET_ACCESS_KEY",  # Fixed missing comma
            region_name="us-east-1"
        )

        bucket_name = "your-bucket-name"
        
        # Updated utcnow() to timezone-aware datetime
        timestamp = datetime.now(timezone.utc).strftime("%Y%m%d_%H%M%S")
        file_key = f"raw/flight_data_{timestamp}.json"

        # 3. Stream data to S3 using boto3
        s3_client.put_object(
            Bucket=bucket_name,
            Key=file_key,
            Body=json.dumps(raw_data),
            ContentType="application/json"
        )
        print(f"Successfully uploaded raw batch via boto3 to s3://{bucket_name}/{file_key}")

    extract_and_upload_to_s3_boto3()

# Instantiate the DAG
flight_ingestion_dag = pipeline()

# Local IDE Test Runner
if __name__ == "__main__":
    print("🚀 Triggering the Airflow DAG locally via IDE Test Mode...")
    flight_ingestion_dag.test()
    print("✅ Local run completed successfully!")
