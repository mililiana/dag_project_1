import datetime
from airflow import DAG
from airflow.datasets import Dataset
from airflow.operators.python import PythonOperator
from airflow.providers.postgres.hooks.postgres import PostgresHook
from create_tables_postgres import create_dim_weather_table, create_dim_calendar_table, create_dim_season_table, create_dim_wind_speed_table, create_dim_temp_table, create_count_bikes_table
from insert_data_postgres import insert_weather_data, insert_season_data, insert_temp_data, insert_wind_data, insert_calendar_data
from aggregate_data_postgres import aggregate_and_insert_fact_data

with DAG(
    dag_id="postgres_pipeline",
    start_date=datetime.datetime(2020, 2, 2),
    schedule= [Dataset("bike_rental.dim_calendar"),
        Dataset("bike_rental.dim_weather_category"),
        Dataset("bike_rental.dim_windspeed_category"),
        Dataset("bike_rental.dim_temp_category"),
        Dataset("bike_rental.dim_season_category")],
    catchup=False,
) as dag:
    create_weather_table = PythonOperator(
        task_id="create_dim_weather_table",
        python_callable=create_dim_weather_table,
    )
    create_calendar_table = PythonOperator(
        task_id='create_dim_calendar_table',
        python_callable=create_dim_calendar_table,
    ) 
    create_season_table = PythonOperator(
        task_id='create_dim_season_table',
        python_callable=create_dim_season_table,
    )
    create_dim_wind_speed_table = PythonOperator(
        task_id='create_dim_wind_speed_table',
        python_callable=create_dim_wind_speed_table,
    )
    create_dim_temp_table = PythonOperator(
        task_id='create_dim_temp_table',
        python_callable=create_dim_temp_table,
    )
    create_fact_table = PythonOperator(
        task_id='create_fact_table',
        python_callable=create_count_bikes_table,
    )
    insert_weather_data = PythonOperator(
        task_id='insert_weather_data',
        python_callable=insert_weather_data,
    )
    insert_season_data = PythonOperator(
        task_id='insert_season_data',
        python_callable=insert_season_data,
    )
    insert_temp_data = PythonOperator(
        task_id='insert_temp_data',
        python_callable=insert_temp_data,
    )
    insert_wind_data = PythonOperator(
        task_id='insert_wind_data',
        python_callable=insert_wind_data,
    )
    insert_calendar_data = PythonOperator(
        task_id='insert_calendar_data',
        python_callable=insert_calendar_data,
    )
    aggregate_and_insert_fact_data = PythonOperator(
        task_id='aggregate_and_insert_fact_data',
        python_callable=aggregate_and_insert_fact_data,
    )


(
    create_weather_table >> insert_weather_data,
    create_calendar_table >> insert_calendar_data,
    create_season_table >> insert_season_data,
    create_dim_wind_speed_table >> insert_wind_data,
    create_dim_temp_table >> insert_temp_data
) >> create_fact_table >> aggregate_and_insert_fact_data




