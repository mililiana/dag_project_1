import json
import os
from airflow.hooks.postgres_hook import PostgresHook
from airflow.models import Variable


def create_dim_weather_table():
    hook = PostgresHook(postgres_conn_id="postgres_local")
    conn = hook.get_conn()
    cursor = conn.cursor()
    
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS dim_weather_category (
            weather_code INT PRIMARY KEY,
            weather_desc TEXT
        );
    """)
    conn.commit()
    cursor.close()
    conn.close()

def create_dim_calendar_table():
    hook = PostgresHook(postgres_conn_id="postgres_local")
    conn = hook.get_conn()
    cursor = conn.cursor()
    
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS dim_calendar (
            dim_calendar_id SERIAL PRIMARY KEY,
            is_working_day BOOLEAN NOT NULL,
            is_holiday BOOLEAN NOT NULL,
            day_of_week INT NOT NULL,
            month INT NOT NULL,
            day INT NOT NULL,
            year INT NOT NULL,
            CONSTRAINT unique_date UNIQUE (year, month, day)
        );

    """)
    
    conn.commit()
    cursor.close()
    conn.close()


def create_dim_season_table():
    hook = PostgresHook(postgres_conn_id="postgres_local")
    conn = hook.get_conn()
    cursor = conn.cursor()
    
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS dim_season_category (
            season_code INT PRIMARY KEY,
            season_desc TEXT
        );
    """)
    
    conn.commit()
    cursor.close()
    conn.close()

def create_dim_wind_speed_table():
    hook = PostgresHook(postgres_conn_id="postgres_local")
    conn = hook.get_conn()
    cursor = conn.cursor()

    cursor.execute("""
        CREATE TABLE IF NOT EXISTS dim_wind_speed_category (
            category_id SERIAL PRIMARY KEY,
            wind_category TEXT UNIQUE
        );
    """)    
    conn.commit()
    cursor.close()
    conn.close()



def create_dim_temp_table():
    hook = PostgresHook(postgres_conn_id="postgres_local")
    conn = hook.get_conn()
    cursor = conn.cursor()

    cursor.execute("""
        CREATE TABLE IF NOT EXISTS dim_temp_category (
            category_id SERIAL PRIMARY KEY,
            temp_category TEXT UNIQUE
        );
    """)
    conn.commit()
    cursor.close()
    conn.close()


def create_count_bikes_table():
    hook = PostgresHook(postgres_conn_id="postgres_local")
    conn = hook.get_conn()
    cursor = conn.cursor()

    cursor.execute("""
        CREATE TABLE IF NOT EXISTS fact_count_bikes (
            id SERIAL PRIMARY KEY,

            general_cnt_bike INT NOT NULL,
            cnt_bike_no_registration INT NOT NULL,
            cnt_bike_with_registration INT NOT NULL,

            season_code INT,
            wind_category_id INT,
            temp_category_id INT,
            calendar_id INT,
            weather_code INT,

            FOREIGN KEY (season_code) REFERENCES dim_season_category(season_code),
            FOREIGN KEY (wind_category_id) REFERENCES dim_wind_speed_category(category_id),
            FOREIGN KEY (temp_category_id) REFERENCES dim_temp_category(category_id),
            FOREIGN KEY (calendar_id) REFERENCES dim_calendar(dim_calendar_id),
            FOREIGN KEY (weather_code) REFERENCES dim_weather_category(weather_code)


        
        );
    """)

    conn.commit()
    cursor.close()
    conn.close()


