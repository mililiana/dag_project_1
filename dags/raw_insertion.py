# import json
# import pandas as pd
# from sqlalchemy import create_engine

# engine = create_engine("postgresql://airflow:airflow@localhost:5432/airflow")


# with open("/Users/lilianamirchuk/Desktop/6_семетр/АСД/airflow-my-first/dags/data/fact_bike_rentals.json", "r") as f:
#     data = json.load(f)
# df = pd.DataFrame(data)

# df.to_sql("raw_data_table", con=engine, if_exists="replace", index=False)

# print("Сирі дані завантажено в таблицю raw_data_table!")
