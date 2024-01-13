from airflow import DAG
from airflow.operators.python import PythonOperator
from datetime import datetime
from datetime import timedelta
from airflow.providers.postgres.operators.postgres import PostgresOperator
from airflow.providers.amazon.aws.transfers.s3_to_sql import S3ToSqlOperator
from airflow.providers.amazon.aws.transfers.local_to_s3 import LocalFilesystemToS3Operator

with DAG(
    dag_id = "dag_s3_test",
    schedule="@hourly",
    default_args={
        "owner":"airflow",
        "start_date":datetime(2024,1,8)
    },
    catchup=False,
) as f:  
  
    create_local_to_s3_job = LocalFilesystemToS3Operator(
        task_id="create_local_to_s3_job",
        filename="/home/kiwichi/Downloads/all_uploadtest",
        dest_key="upload",
        dest_bucket="meteobucketfirst",
        replace=True,
        aws_conn_id="aws_connection_jordi"
    )