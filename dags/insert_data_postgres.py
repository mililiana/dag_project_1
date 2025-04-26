import json
import os
from airflow.hooks.postgres_hook import PostgresHook
from airflow.models import Variable

def insert_weather_data():
    hook = PostgresHook(postgres_conn_id="postgres_local")
    conn = hook.get_conn()
    cursor = conn.cursor()

    with open("/opt/airflow/dags/data/dim_weather_category.json", "r") as f:
        weather_data = json.load(f)

    for row in weather_data:
        cursor.execute("""
            INSERT INTO dim_weather_category (weather_code, weather_desc)
            VALUES (%s, %s)
            ON CONFLICT (weather_code) DO NOTHING;
        """, (row["weather_code"], row["weather_desc"]))

    conn.commit()
    cursor.close()
    conn.close()


def insert_season_data():
    hook = PostgresHook(postgres_conn_id="postgres_local")
    conn = hook.get_conn()
    cursor = conn.cursor()

    with open("/opt/airflow/dags/data/dim_season_category.json", "r") as f:
        weather_data = json.load(f)

    for row in weather_data:
        cursor.execute("""
            INSERT INTO dim_season_category (season_code, season_desc)
            VALUES (%s, %s)
            ON CONFLICT (season_code) DO NOTHING;
        """, (row["season_code"], row["season_desc"]))

    conn.commit()
    cursor.close()
    conn.close()


def insert_temp_data():
    hook = PostgresHook(postgres_conn_id="postgres_local")
    conn = hook.get_conn()
    cursor = conn.cursor()

    with open("/opt/airflow/dags/data/dim_temp_category.json", "r") as f:
        weather_data = json.load(f)

    for row in weather_data:
        cursor.execute("""
            INSERT INTO dim_temp_category (temp_category)
            VALUES (%s)
            ON CONFLICT (temp_category) DO NOTHING;
        """, (row["temp_category"],))

    conn.commit()
    cursor.close()
    conn.close()

def insert_wind_data():
    hook = PostgresHook(postgres_conn_id="postgres_local")
    conn = hook.get_conn()
    cursor = conn.cursor()

    with open("/opt/airflow/dags/data/dim_wind_speed.json", "r") as f:
        wind_data = json.load(f)

    for row in wind_data:
        cursor.execute("""
            INSERT INTO dim_wind_speed_category (wind_category)
            VALUES (%s)
            ON CONFLICT (wind_category) DO NOTHING;
        """, (row["wind_category"],))  

    conn.commit()
    cursor.close()
    conn.close()


def insert_calendar_data():
    hook = PostgresHook(postgres_conn_id="postgres_local")
    conn = hook.get_conn()
    cursor = conn.cursor()

    with open("/opt/airflow/dags/data/dim_calendar.json", "r") as f:
        calendar_data = json.load(f)

    for row in calendar_data:
        cursor.execute("""
            INSERT INTO dim_calendar (is_working_day, is_holiday, day_of_week, month, day, year)
            VALUES (CAST(%s AS BOOLEAN), CAST(%s AS BOOLEAN), %s, %s, %s, %s)
            ON CONFLICT (year, month, day) DO NOTHING;
        """, (row["is_working_day"], row["is_holiday"], row["day_of_week"], row["month"], row["day"], row["year"]))

    conn.commit()
    cursor.close()
    conn.close()


