# 🚲 Bike Rental Data Pipeline Project

## 📋 Project Overview
This project builds an **ETL pipeline** for processing bike rental data using **Apache Airflow**.  

You can find the **original dataset** here: [Bike Sharing Dataset (Regression) on Kaggle](https://www.kaggle.com/datasets/ayessa/bike-sharing-dataset-regression).

It is designed to:
- Extract and transform raw rental data into structured **dimension** and **fact tables**.
- Save processed outputs into **JSON** files.
- Automate the entire flow using **Apache Airflow DAGs**.

---

## Technology Stack
- **Python 3.12**
- **Apache Airflow 2.9+**
- **Docker**
- **Pandas**
- **JSON**

---

## How to Set Up and Run

### 1. Clone the repository
```bash
git clone https://github.com/your-username/your-repo-name.git
cd your-repo-name
```

### 2. Launch Apache Airflow with Docker
Make sure you have **Docker** and **Docker Compose** installed.

To start Airflow:
```bash
docker-compose up -d
```

This will:
- Set up Airflow Webserver (localhost:8080)
- Set up Airflow Scheduler
- Set up Airflow Metadata Database (Postgres)

You can access the Airflow UI at [http://localhost:8080](http://localhost:8080).

**Default credentials:**
- Username: `airflow`
- Password: `airflow`

> If you need to create the airflow database and admin user manually, run:
> ```bash
> docker-compose run --rm airflow-init
> ```


### 3. Set up the DAG
- Go to the Airflow UI.
- Enable the `bike_rental_pipeline` DAG.
- Trigger it manually or schedule it automatically.

### 4. Output
After running the DAG successfully, the transformed `.json` files will appear in the `output/` folder.

---

## Explanation of Tables

- **Dimension Tables (`dim`)**:
  - `dim_calendar.json` — Info about dates: working days, holidays, weekdays.
  - `dim_season_category.json` — Seasons (Winter, Spring, etc.).
  - `dim_weather_category.json` — Weather conditions mapping.
  - `dim_temp_category.json` — Temperature categories.
  - `dim_windspeed_category.json` — Windspeed categories.

- **Fact Table (`fact`)**:
  - `fact_bike_rentals.json` — Aggregated bike rental counts (`general_cnt_bike`, `cnt_bike_no_registration`, `cnt_bike_with_registration`).

Each fact table entry can be joined with dimension tables via common keys like `season_code`, `weather_code`, `date`, etc., during analysis.

---

## Notes
- This project **prepares** the data for future analytical tasks (e.g., loading into a data warehouse or building a dashboard).
- You can extend the project by:
  - Adding database connections (Postgres, Snowflake, etc.).
  - Setting up scheduled daily ingestion.
  - Building dashboards with PowerBI, Tableau, or Superset.

---

## 📢 Author
Developed by [Liliana Mirchuk]  
