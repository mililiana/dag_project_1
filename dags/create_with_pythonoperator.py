from airflow import DAG
from airflow.operators.python import PythonOperator
from datetime import datetime, timedelta


default_args = {
    'owner': 'coder2j',
    'retries': 5,
    'retry_delay': timedelta(minutes=5)
}

def say_hello():
    print("Hello from PythonOperator!")

with DAG(
    default_args=default_args,
    dag_id='our_dag_with_python_operator_v01',
    description='pythonOperator',
    start_date=datetime(2021, 10, 6),
    schedule_interval='@daily'
) as dag:

    task1 = PythonOperator(
        task_id='say_hello_task',
        python_callable=say_hello
    )

    task1
