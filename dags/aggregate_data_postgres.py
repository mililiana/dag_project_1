from airflow.providers.postgres.hooks.postgres import PostgresHook

def aggregate_and_insert_fact_data():
    hook = PostgresHook(postgres_conn_id="postgres_local")
    conn = hook.get_conn()
    cursor = conn.cursor()

    query = """
            INSERT INTO fact_count_bikes (
            general_cnt_bike,
            cnt_bike_no_registration,
            cnt_bike_with_registration,
            season_code,
            wind_category_id,
            temp_category_id,
            calendar_id,
            weather_code
        )
        SELECT 
            r.general_cnt_bike,
            r.cnt_bike_no_registration,
            r.cnt_bike_with_registration,
            s.season_code,
            ws.category_id,
            t.category_id,
            cal.dim_calendar_id,
            w.weather_code

        FROM raw_data_table r

        JOIN dim_season_category s ON s.season_code = r.season_id
        JOIN dim_weather_category w ON w.weather_code = r.weather_id

        -- Temperature categorization (matching Python logic: *47 - 8)
        JOIN dim_temp_category t ON t.temp_category = (
            CASE
                WHEN (r.temperature_id * 47 - 8) < 5 THEN 'Cold'
                WHEN (r.temperature_id * 47 - 8) < 15 THEN 'Cool'
                WHEN (r.temperature_id * 47 - 8) < 25 THEN 'Warm'
                ELSE 'Hot'
            END
        )

        -- Wind categorization (matching Python logic: *67)
        JOIN dim_wind_speed_category ws ON ws.wind_category = (
            CASE
                WHEN (r.wind_speed_id * 67) < 10 THEN 'Low wind'
                WHEN (r.wind_speed_id * 67) < 25 THEN 'Average wind'
                WHEN (r.wind_speed_id * 67) < 40 THEN 'Strong winds'
                ELSE 'Very strong winds'
            END
        )

        -- Calendar join
        JOIN dim_calendar cal ON
            cal.year = FLOOR(r.date_id / 10000) AND
            cal.month = FLOOR((r.date_id % 10000) / 100) AND
            cal.day = r.date_id % 100

    """

    cursor.execute(query)
    conn.commit()
    cursor.close()
    conn.close()
