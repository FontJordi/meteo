from airflow import DAG
from airflow.operators.python import PythonOperator
from datetime import datetime
from datetime import timedelta
from airflow.providers.postgres.operators.postgres import PostgresOperator
from airflow.providers.amazon.aws.transfers.s3_to_sql import S3ToSqlOperator
from airflow.providers.amazon.aws.hooks.s3 import S3Hook
import boto3
from airflow.operators.bash import BashOperator
import time
from airflow.providers.postgres.hooks.postgres import PostgresHook

#ugly function, should use the same method as the transfer_untransfered_csv_to_postgres to transfer files
def get_latest_object(bucket_name, prefix):
    """Retrieves the S3 object with the latest last modified timestamp."""

    s3_hook = S3Hook(aws_conn_id="aws_connection")  # Replace with your connection ID
    response = s3_hook.list_keys(bucket_name=bucket_name, prefix=prefix)

    # Get the object with the latest last modified timestamp
    latest_object = max(response)

    # Return the key (i.e., object path) of the latest object
    return latest_object



def log_latest_s3_object(**kwargs):
    ti = kwargs['ti']
    latest_s3_object = ti.xcom_pull(task_ids='create_meteo_hist_table')
    print(f"The latest S3 object is: {latest_s3_object}")


def parse_csv_to_list(filepath):
    import csv

    with open(filepath, newline="") as file:
        return list(csv.reader(file))           

with DAG(
    dag_id = "EXTRACT_S3_DAG",
    schedule="@hourly",
    default_args={
        "owner":"airflow",
        "start_date":datetime(2024,1,8)
    },
    catchup=False,
) as dag:

    first_function = BashOperator(
        task_id="first_function",
        bash_command='python /opt/airflow/additional-data/script.py'
    )

    create_schema = PostgresOperator(
        task_id="create_schema",
        sql="""CREATE SCHEMA IF NOT EXISTS weatherapi;""",
        postgres_conn_id='postgres_rds_connection',
        database="mydb"
    )
        
    create_meteo_table = PostgresOperator(
        task_id="create_meteo_table",
        sql="""
            CREATE TABLE IF NOT EXISTS weatherapi.meteo_insert (
            coord_lon                 VARCHAR,
            coord_lat                 VARCHAR,
            weather_id                VARCHAR,
            weather_main              VARCHAR,
            weather_description       VARCHAR,
            weather_icon              VARCHAR,
            base                      VARCHAR,
            main_temp                 VARCHAR,
            main_feels_like           VARCHAR,
            main_temp_min             VARCHAR,
            main_temp_max             VARCHAR,
            main_pressure             VARCHAR,
            main_humidity             VARCHAR,
            main_sea_level            VARCHAR,
            main_grnd_level           VARCHAR,
            visibility                VARCHAR,
            wind_speed                VARCHAR,
            wind_deg                  VARCHAR,
            sys_type                  VARCHAR,
            sys_id                    VARCHAR,
            sys_country               VARCHAR,
            sys_sunrise               VARCHAR,
            sys_sunset                VARCHAR,
            timezone                  VARCHAR,
            id                        VARCHAR,
            name                      VARCHAR,
            cod                       VARCHAR,
            rain_1h                   VARCHAR,
            rain_3h                   VARCHAR, 
            snow_1h                   VARCHAR,
            snow_3h                   VARCHAR,
            insertdatetime            VARCHAR,
            PRIMARY KEY (name, dt));
          """,
          postgres_conn_id='postgres_rds_connection',
          database="mydb"
    ) 

    latest_s3_object = get_latest_object("meteobucketfirst", "historical/meteo/ES")

    #log_latest_s3_object_task = PythonOperator(
    #    task_id="log_latest_s3_object",
    #    python_callable=log_latest_s3_object,
    #    provide_context=True
    #)


    delay_python_task = PythonOperator(
        task_id="delay_python_task",
        dag=dag,
        python_callable=lambda: time.sleep(10))


    transfer_s3_to_sql = S3ToSqlOperator(
        task_id="transfer_s3_to_sql",
        s3_bucket="meteobucketfirst",
        s3_key=get_latest_object("meteobucketfirst", "historical/meteo/ES"),  #"historical/ES/all",
        table="weatherapi.meteo_insert",
        #schema="weatherapi",
        column_list=['coord_lon', 'coord_lat', 'weather_id', 'weather_main',
        'weather_description', 'weather_icon', 'base', 'main_temp',
        'main_feels_like', 'main_temp_min', 'main_temp_max', 'main_pressure',
        'main_humidity', 'main_sea_level', 'main_grnd_level', 'visibility',
        'wind_speed', 'wind_deg', 'wind_gust', 'clouds_all', 'dt', 'sys_type',
        'sys_id', 'sys_country', 'sys_sunrise', 'sys_sunset', 'timezone', 'id',
        'name','cod','rain_1h','rain_3h', 'snow_1h','snow_3h','insertdatetime'],
        parser=parse_csv_to_list,
        sql_conn_id='postgres_rds_connection',
        aws_conn_id='aws_connection',
    )

    #run_dbt_model = BashOperator(
    #task_id='run_dbt_model',
    #bash_command='pushd /home/kiwichi/dbt-testing/dbt_core_demo; source /home/kiwichi/dbt-testing/dbt-env/bin/activate; dbt run; popd',
    #dag=dag
    #)

    first_function >> create_schema  >> create_meteo_table >> delay_python_task >> transfer_s3_to_sql# >> run_dbt_model
        