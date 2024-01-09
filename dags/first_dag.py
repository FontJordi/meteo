from airflow import DAG
from airflow.operators.bash import BashOperator
from datetime import datetime
from datetime import timedelta

with DAG(
    dag_id = "first_dag",
    schedule="@hourly",
    default_args={
        "owner":"airflow",
        "retries":1,
        "retry_delay":timedelta(minutes=1),
        "start_date":datetime(2024,1,8)
    },
    catchup=False,
) as f:
    
    first_function = BashOperator(
        task_id="first_func_execute",
        bash_command='/bin/python3 /home/kiwichi/WEATHERAPI/script/script.py'
    )