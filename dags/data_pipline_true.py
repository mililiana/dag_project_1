from airflow import DAG
from airflow.sensors.filesystem import FileSensor
from airflow.operators.python import PythonOperator
from airflow.datasets import Dataset
from airflow.models import Variable
import datetime
import pendulum
import json
import os
import pandas as pd
from airflow.hooks.base import BaseHook
from datasets_true import create_dim_calendar , create_dim_weather_category, create_dim_windspeed_category, create_dim_temp_category, create_dim_season_category, create_fact_bike_rentals


dag = DAG(
    dag_id="bike_rental_pipeline",
    schedule="*/1 * * * *",
    start_date=pendulum.datetime(2025, 3, 18),
    catchup=False,
    dagrun_timeout=datetime.timedelta(minutes=60),
)

check_raw_data = FileSensor(
    task_id="check_raw_data_file",
    filepath=Variable.get('bike_rental_raw_file'),
    fs_conn_id="bike_rental_data",
    poke_interval=10,
    timeout=60,
    dag=dag 
)

create_dim_calendar_task = PythonOperator(
    task_id="create_dim_calendar",
    python_callable=create_dim_calendar,
    outlets=[Dataset("bike_rental.dim_calendar")],  
    dag=dag
)

create_dim_weather_category_task = PythonOperator(
    task_id="create_dim_weather_category",
    python_callable=create_dim_weather_category,
    outlets=[Dataset("bike_rental.dim_weather_category")],
    dag=dag
)

create_dim_windspeed_category_task = PythonOperator(
    task_id="create_dim_windspeed_category",
    python_callable=create_dim_windspeed_category,
    outlets=[Dataset("bike_rental.dim_windspeed_category")],
    dag=dag
)

create_dim_temp_category_task = PythonOperator(
    task_id="create_dim_temp_category",
    python_callable=create_dim_temp_category,
    outlets=[Dataset("bike_rental.dim_temp_category")],
    dag=dag
)

create_dim_season_category_task = PythonOperator(
    task_id="create_dim_season_category",
    python_callable=create_dim_season_category,
    outlets=[Dataset("bike_rental.dim_season_category")],
    dag=dag
)


create_fact_bike_rentals_task = PythonOperator(
    task_id="create_dim_count_bikes",
    python_callable=create_fact_bike_rentals,
    outlets=[Dataset("bike_rental.dim_count_bikes")],
    dag=dag
)



check_raw_data >> [
    create_dim_calendar_task,
    create_dim_weather_category_task,
    create_dim_windspeed_category_task,
    create_dim_temp_category_task,
    create_dim_season_category_task, 
    create_fact_bike_rentals_task
]
