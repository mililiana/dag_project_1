import json
from airflow import DAG
from airflow.operators.python_operator import PythonOperator
from airflow.providers.postgres.hooks.postgres import PostgresHook
from airflow.models import Variable
from datetime import datetime
from datetime import datetime, timedelta
import pendulum
from airflow import DAG

# Функція для створення таблиць у PostgreSQL
def create_tables():
    pg_hook = PostgresHook(postgres_conn_id="postgres_conn_id")
    conn = pg_hook.get_conn()
    cursor = conn.cursor()
    
    create_sql = """
    CREATE TABLE IF NOT EXISTS Location (
        Location_ID SERIAL PRIMARY KEY,
        region TEXT,
        settlement TEXT
    );

    CREATE TABLE IF NOT EXISTS Unit (
        Unit_ID SERIAL PRIMARY KEY,
        unit_name TEXT
    );

    CREATE TABLE IF NOT EXISTS Rank (
        Rank_ID SERIAL PRIMARY KEY,
        rank_name TEXT
    );

    CREATE TABLE IF NOT EXISTS Death_Location (
        Death_Location_ID SERIAL PRIMARY KEY,
        death_district TEXT,
        death_settlement TEXT
    );

    CREATE TABLE IF NOT EXISTS Date_of_death (
        Date_of_death_ID SERIAL PRIMARY KEY,
        date_of_death DATE
    );

    CREATE TABLE IF NOT EXISTS Facts (
        Fact_ID SERIAL PRIMARY KEY,
        Location_ID INT REFERENCES Location(Location_ID),
        Unit_ID INT REFERENCES Unit(Unit_ID),
        Rank_ID INT REFERENCES Rank(Rank_ID),
        Death_Location_ID INT REFERENCES Death_Location(Death_Location_ID),
        Date_of_death_ID INT REFERENCES Date_of_death(Date_of_death_ID),
        count_of_death INT
    );
    """
    
    cursor.execute(create_sql)
    conn.commit()
    cursor.close()
    conn.close()

