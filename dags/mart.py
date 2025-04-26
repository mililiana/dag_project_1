import os
import logging
import psycopg2
from airflow import DAG
from airflow.operators.python import PythonOperator
from datetime import datetime


def execute_sql_file_and_log_rows(table_name: str, sql_file_path: str):
    conn = psycopg2.connect(
        dbname="airflow",
        user="airflow",
        password="airflow",
        host="host.docker.internal",
        port="5432"
    )
    cursor = conn.cursor()

    with open(sql_file_path, 'r') as file:
        sql_script = file.read()
    cursor.execute(sql_script)
    conn.commit()

    cursor.execute(f"SELECT COUNT(*) FROM {table_name}")
    row_count = cursor.fetchone()[0]
    logging.info(f"[{table_name}] Row count: {row_count}")

    cursor.close()
    conn.close()


with DAG(
    dag_id="build_data_mart_python",
    start_date=datetime(2024, 1, 1),
    # schedule_interval="*/1 * * * *",  
    schedule_interval="@monthly",
    catchup=False,
    tags=["marts"],
) as dag:

    marts = {
        "mart_bike_rentals_by_weather": "dags/sql/create_mart_bike_rentals_by_weather.sql",
        "mart_bike_rentals_by_season_and_daytype": "dags/sql/mart_bike_rentals_by_season_and_daytype.sql",
        "mart_bike_rentals_by_season": "dags/sql/mart_bike_rentals_by_season.sql",
        "mart_bike_rentals_by_temperature": "dags/sql/mart_bike_rentals_by_temperature.sql", 
        "mart_bike_rentals_by_weather_and_daytype": "dags/sql/mart_bike_rentals_by_weather_and_daytype.sql",
        "mart_bike_rentals_working_vs_weekend_extended": "dags/sql/mart_bike_rentals_working_vs_weekend_extended.sql",
        "mart_bike_rentals_working_vs_weekend": "dags/sql/mart_bike_rentals_working_vs_weekend.sql",

    }

    for mart_name, sql_path in marts.items():
        PythonOperator(
            task_id=f"create_{mart_name}",
            python_callable=execute_sql_file_and_log_rows,
            op_args=[mart_name, sql_path],
        )

