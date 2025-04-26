from airflow import DAG
from airflow.sensors.filesystem import FileSensor
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
    dag_id="bike_rental_pipeline_second",
    schedule="*/1 * * * *",
    start_date=pendulum.datetime(2025, 3, 18),
    catchup=False,
    dagrun_timeout=datetime.timedelta(minutes=60),
)

