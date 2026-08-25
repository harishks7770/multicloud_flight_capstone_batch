from datetime import datetime, timedelta
import json
import boto3
import requests
from airflow.decorators import dag, task

default_args = {
    "owner": "multi_cloud_dev",
    "retries": 1,
    "retry_delay": timedelta(minutes=5),
}

@dag(
    dag_id="multicloud_flight_ingestion_boto3",
    default_args=default_args,
    schedule_interval="@daily",
    start_date=datetime(2026, 1, 1),
    catchup=False,
    tags=["azure", "aws", "snowflake", "boto3"],
)
def pipeline():

    @task()
    def extract_and_upload_to_s3_boto3():
        # 1. Fetch raw data from OpenSky
        url = "https://opensky-network.org/api/states/all"
        res = requests.get(url)
        if res.status_code != 200:
            raise ValueError(f"API call failed with status: {res.status_code}")

        raw_data = res.json()

        # 2. Initialize boto3 S3 client
        # 🔴 UPDATE THESE THREE LINES WITH YOUR AWS DETAILS
        s3_client = boto3.client(
            "s3",
            aws_access_key_id="<your_access_key_id",
            aws_secret_access_key="<yout_secret_access_key>"
            region_name="<your_region>"
        )

        bucket_name = "<your_bucket_name>"
        file_key = f"raw/flight_data_{datetime.utcnow().strftime('%Y%m%d_%H%M%S')}.json"

        # 3. Stream data to S3 using boto3
        s3_client.put_object(
            Bucket=bucket_name,
            Key=file_key,
            Body=json.dumps(raw_data)
        )
        print(f"Successfully uploaded raw batch via boto3 to s3://{bucket_name}/{file_key}")

    extract_and_upload_to_s3_boto3()

# Instantiate the DAG
flight_ingestion_dag = pipeline()

# --- THE IDE RUNNER BLOCK ---
if __name__ == "__main__":
    print("🚀 Triggering the Airflow DAG locally via IDE Test Mode...")
    flight_ingestion_dag.test()
    print("✅ Local run completed successfully!")
