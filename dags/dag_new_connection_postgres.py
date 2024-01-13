from airflow.models import Connection
from airflow import settings
from airflow.secrets.local_filesystem import LocalFilesystemBackend
from airflow import DAG
from datetime import datetime

def create_conn(username, password,host=None):

    new_conn = Connection(  
        conn_id='postgres_rds_connection',
        conn_type='postgres',
        login=username,
        host=host if host else None,
        password = password,
        port = 5432)


    session = settings.Session()
    session.add(new_conn)
    session.commit()


with DAG(
    dag_id = "connection_postgres_dag",
    schedule="@once",
    default_args={
        "owner":"airflow",
        "start_date":datetime(2024,1,8)
    },
    catchup=False,
) as f:
    
    create_conn("wichi", "SuperSafePassword99!!",host="terraform-20240109143437586600000001.cpqeu6wm013d.eu-west-1.rds.amazonaws.com")
