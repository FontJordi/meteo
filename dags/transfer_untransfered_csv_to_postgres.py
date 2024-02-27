from airflow import DAG
from airflow.operators.python import PythonOperator
from datetime import datetime, timedelta
from airflow.providers.postgres.operators.postgres import PostgresOperator
from airflow.providers.amazon.aws.transfers.s3_to_sql import S3ToSqlOperator
from airflow.providers.amazon.aws.hooks.s3 import S3Hook
from airflow.providers.postgres.hooks.postgres import PostgresHook

# Define functions

def parse_csv_to_list(filepath):
    import csv
    with open(filepath, newline="") as file:
        return list(csv.reader(file))    

def create_kafka_schema_if_not_exists(**kwargs):
    sql = """CREATE SCHEMA IF NOT EXISTS kafka;"""
    PostgresOperator(
        task_id="create_schema",
        sql=sql,
        postgres_conn_id='postgres_rds_connection',
        database="mydb"
    ).execute(context=kwargs)

def create_kafka_table_if_not_exists(table_name, columns, **kwargs):
    create_table_query = f"""
        CREATE TABLE IF NOT EXISTS kafka.{table_name} (
            {', '.join(columns)}
        )
    """
    PostgresOperator(
        task_id=f'create_kafka_table_{table_name}_task',
        database="mydb",
        sql=create_table_query,
        postgres_conn_id='postgres_rds_connection',
        dag=dag,
    ).execute(context=kwargs)

def transfer_untransferred_files_to_s3(s3_bucket, s3_prefix, **kwargs):
    s3_hook = S3Hook(aws_conn_id='aws_connection_jordi')
    postgres_hook = PostgresHook(postgres_conn_id='postgres_rds_connection')

    # Get list of files from S3
    files_s3 = s3_hook.list_keys(bucket_name=s3_bucket, prefix=s3_prefix)
    
    # Get list of transferred files from PostgreSQL
    transferred_files_query = """SELECT file_name FROM kafka.files"""
    transferred_files = postgres_hook.get_records(transferred_files_query)

    # Filter files that have not been transferred
    to_transfer = [file for file in files_s3 if file.endswith('.csv') and file not in transferred_files]

    for i, file_name in enumerate(to_transfer):
        # Transfer file to PostgreSQL
        S3ToSqlOperator(
            task_id=f'transfer_file_to_postgres_streaming_{i}',
            s3_bucket=s3_bucket,
            s3_key=file_name,
            table='kafka.data',
            column_list=['fakeTimestamp', 'fakeKey', 'fakeValue'],
            sql_conn_id='postgres_rds_connection',
            aws_conn_id='aws_connection_jordi',
            parser=parse_csv_to_list,
            dag=dag,
        ).execute(context=kwargs)

        # Insert file name into kafka.files table
        PostgresOperator(
            task_id=f'insert_file_name_to_postgres_{i}',
            sql=f"INSERT INTO kafka.files (file_name) VALUES ('{file_name}')",
            postgres_conn_id='postgres_rds_connection',
            dag=dag,
        ).execute(context=kwargs)

# Define default arguments
default_args = {
    'owner': 'airflow',
    'depends_on_past': False,
    'start_date': datetime(2024, 1, 1),
    'email_on_failure': False,
    'email_on_retry': False,
    'retries': 0
}

# Define DAG
dag = DAG(
    'transfer_untransferred_csv_to_postgres',
    default_args=default_args,
    description='A DAG to transfer untransferred csv files from S3 to PostgreSQL',
    schedule_interval='*/5 * * * *',  # Every 5 minutes,
    catchup=False
)

# Define tasks
create_kafka_schema_task = PythonOperator(
    task_id='create_schema',
    python_callable=create_kafka_schema_if_not_exists,
    provide_context=True,
    dag=dag,
)

create_kafka_files_table_task = PythonOperator(
    task_id='create_kafka_files_table',
    python_callable=create_kafka_table_if_not_exists,
    op_kwargs={'table_name': 'files', 'columns': ['file_name VARCHAR(255)', 'created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP']},
    provide_context=True,
    dag=dag,
)

create_kafka_data_table_task = PythonOperator(
    task_id='create_kafka_data_table',
    python_callable=create_kafka_table_if_not_exists,
    op_kwargs={'table_name': 'data', 'columns': ['fakeTimestamp VARCHAR(255)', 'fakeKey VARCHAR(255)', 'fakeValue VARCHAR(255)', 'created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP']},
    provide_context=True,
    dag=dag,
)

transfer_task = PythonOperator(
    task_id='transfer_untransferred_files',
    python_callable=transfer_untransferred_files_to_s3,
    op_args=["meteobucketfirst", "spark/data/2024-02-27"],
    provide_context=True,
    dag=dag,
)

# Define task dependencies
create_kafka_schema_task >> create_kafka_files_table_task >> create_kafka_data_table_task >> transfer_task
