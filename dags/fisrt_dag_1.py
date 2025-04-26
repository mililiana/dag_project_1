from airflow import DAG
from datetime import datetime, timedelta
from airflow.operators.bash import BashOperator

default_args = {
    'owner': 'coder2',
    'retries': 5,
    'retry_delay':  timedelta(minutes=2)
}

with DAG(
    dag_id='my_first_dag',
    default_args=default_args, 
    description='This is first dag',
    start_date=datetime(2011, 2, 14, 2),
    schedule_interval='@daily'

) as dag:
    task1 = BashOperator(
        task_id='first_task', 
        bash_command='echo hello world'
    )
    task2 = BashOperator(
        task_id='second_task', 
        bash_command='second_task'
    )


task1.set_downstream(task2)