import os
import pandas as pd
from airflow.models import Variable

FILE_PATH = Variable.get('bike_rental_raw_file')
df = pd.read_csv(FILE_PATH)






WEATHER_DICT = {
    1: "Clear, Few clouds, Partly cloudy",
    2: "Mist + Cloudy, Mist + Broken clouds, Mist + Few clouds, Mist",
    3: "Light Snow, Light Rain + Thunderstorm + Scattered clouds, Light Rain + Scattered clouds",
    4: "Heavy Rain + Ice Pellets + Thunderstorm + Mist, Snow + Fog"
}

def create_dim_weather_category():
    dim_weather_category = pd.DataFrame({'weather_code': WEATHER_DICT.keys(), 
                                         'weather_desc': WEATHER_DICT.values()})
    output_path = os.path.join(os.path.dirname(FILE_PATH), "dim_weather_category.json")
    dim_weather_category.to_json(output_path, index=False, orient="records", indent=4)
    print(f"Файл збережено: {output_path}")






SEASON_DICT = {
    1: "Winter",
    2: "Spring",
    3: "Summer",
    4: "Fall"
}

def create_dim_season_category():
    dim_season_category = pd.DataFrame({'season_code': SEASON_DICT.keys(), 
                                        'season_desc': SEASON_DICT.values()})
    output_path = os.path.join(os.path.dirname(FILE_PATH), "dim_season_category.json")
    dim_season_category.to_json(output_path, index=False, orient="records", indent=4)
    print(f"Файл збережено: {output_path}")





def create_dim_calendar():
    df['date'] = pd.to_datetime(df['dteday'])

    dim_calendar = df[['workingday', 'holiday', 'weekday']].copy()
    dim_calendar.rename(columns={'workingday': 'is_working_day', 
                                 'holiday': 'is_holiday', 
                                 'weekday': 'day_of_week'}, inplace=True)

    dim_calendar['month'] = df['date'].dt.month
    dim_calendar['day'] = df['date'].dt.day
    dim_calendar['year'] = df['date'].dt.year


    output_path = os.path.join(os.path.dirname(FILE_PATH), "dim_calendar.json")
    dim_calendar.to_json(output_path, orient="records", indent=4)
    print(f"Файл збережено: {output_path}")




def create_dim_windspeed_category():
    def categorize_windspeed(ws):
        if ws < 10:
            return "Low wind"
        elif ws < 25:
            return "Average wind"
        elif ws < 40:
            return "Strong winds"
        else:
            return "Very strong winds"

    df["real_windspeed"] = df["windspeed"] * 67  
    df["wind_category"] = df["real_windspeed"].apply(categorize_windspeed)

    dim_wind_speed = df[['wind_category']]

    output_path = os.path.join(os.path.dirname(FILE_PATH), "dim_wind_speed.json")
    dim_wind_speed.to_json(output_path, index=False, orient="records", indent=4)
    print(f"Файл збережено: {output_path}")






def create_dim_temp_category():
    def categorize_temp(t):
        if t < 5:
            return "Cold"
        elif t < 15:
            return "Cool"
        elif t < 25:
            return "Warm"
        else:
            return "Hot"

    df["real_temp"] = df["temp"] * 47 - 8 
    df["temp_category"] = df["real_temp"].apply(categorize_temp)

    dim_temp_category = df[['temp_category']].drop_duplicates()

    output_path = os.path.join(os.path.dirname(FILE_PATH), "dim_temp_category.json")
    dim_temp_category.to_json(output_path, index=False, orient="records", indent=4)
    print(f"Файл збережено: {output_path}")




def create_fact_bike_rentals():
    fact_bike_rentals = pd.DataFrame({
        'date_id': pd.to_datetime(df['dteday']).dt.strftime('%Y%m%d').astype(int), 
        'season_id': df['season'],  
        'weather_id': df['weathersit'],
        'wind_speed_id': df['windspeed'],
        'temperature_id': df['temp'],
        'general_cnt_bike': df['cnt'],  
        'cnt_bike_no_registration': df['casual'], 
        'cnt_bike_with_registration': df['registered'] 
    })


    output_path = os.path.join(os.path.dirname(FILE_PATH), "fact_bike_rentals.json")
    fact_bike_rentals.to_json(output_path, index=False, orient="records", indent=4)
    print(f"Файл збережено: {output_path}")

