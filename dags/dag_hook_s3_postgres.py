from airflow import DAG
from airflow.operators.python import PythonOperator
from datetime import datetime
from datetime import timedelta
from airflow.providers.postgres.operators.postgres import PostgresOperator
from airflow.providers.amazon.aws.transfers.s3_to_sql import S3ToSqlOperator


with DAG(
    dag_id = "dag_hook_s3_postgres",
    schedule="@hourly",
    default_args={
        "owner":"airflow",
        "start_date":datetime(2024,1,8)
    },
    catchup=False,
) as f:
    
    def parse_csv_to_list(filepath):
        import csv

        with open(filepath, newline="") as file:
            return list(csv.reader(file))

    create_meteo_table = PostgresOperator(
        task_id="create_meteo_table",
        sql="""
            CREATE TABLE IF NOT EXISTS meteo (
            idcode           VARCHAR PRIMARY KEY,
            coord_lon                 VARCHAR,
            coord_lat                 VARCHAR,
            weather_id                VARCHAR,
            weather_main              VARCHAR,
            weather_description       VARCHAR,
            weather_icon              VARCHAR,
            base                      VARCHAR,
            main_temp VARCHAR,
            main_feels_like VARCHAR,
            main_temp_min VARCHAR,
            main_temp_max VARCHAR,
            main_pressure VARCHAR,
            main_humidity VARCHAR,
            main_sea_level VARCHAR,
            main_grnd_level VARCHAR,
            visibility VARCHAR,
            wind_speed VARCHAR,
            wind_deg VARCHAR,
            wind_gust VARCHAR,
            clouds_all VARCHAR,
            dt VARCHAR,
            sys_type VARCHAR,
            sys_id VARCHAR,
            sys_country VARCHAR,
            sys_sunrise VARCHAR,
            sys_sunset VARCHAR,
            timezone VARCHAR,
            id VARCHAR,
            name VARCHAR,
            cod varchar);
          """,
          postgres_conn_id='postgres_rds_connection',
          database="mydb"
    ) 


    transfer_s3_to_sql = S3ToSqlOperator(
        task_id="transfer_s3_to_sql",
        s3_bucket="meteobucketfirst",
        s3_key="CAT/all",
        table="meteo",
        column_list=['idcode','coord_lon', 'coord_lat', 'weather_id', 'weather_main',
        'weather_description', 'weather_icon', 'base', 'main_temp',
        'main_feels_like', 'main_temp_min', 'main_temp_max', 'main_pressure',
        'main_humidity', 'main_sea_level', 'main_grnd_level', 'visibility',
        'wind_speed', 'wind_deg', 'wind_gust', 'clouds_all', 'dt', 'sys_type',
        'sys_id', 'sys_country', 'sys_sunrise', 'sys_sunset', 'timezone', 'id',
        'name','cod'],
        parser=parse_csv_to_list,
        sql_conn_id='postgres_rds_connection',
        aws_conn_id='aws_connection_jordi',
    )
    create_meteo_table>>transfer_s3_to_sql
          
        
