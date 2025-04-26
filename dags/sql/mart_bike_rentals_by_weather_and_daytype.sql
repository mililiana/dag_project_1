DROP TABLE IF EXISTS mart_bike_rentals_by_weather_and_daytype;
CREATE TABLE mart_bike_rentals_by_weather_and_daytype AS
SELECT
    dw.weather_desc,
    CASE WHEN dc.is_working_day THEN 'Working Day' ELSE 'Weekend / Holiday' END AS day_type,
    COUNT(DISTINCT TO_DATE(dc.year || '-' || LPAD(dc.month::text,2,'0') || '-' || LPAD(dc.day::text,2,'0'), 'YYYY-MM-DD')) AS total_days,
    SUM(fr.cnt_bike_no_registration + fr.cnt_bike_with_registration) AS total_rentals,
    ROUND(SUM(fr.cnt_bike_no_registration + fr.cnt_bike_with_registration) * 1.0 /
          COUNT(DISTINCT TO_DATE(dc.year || '-' || LPAD(dc.month::text,2,'0') || '-' || LPAD(dc.day::text,2,'0'), 'YYYY-MM-DD')), 2) AS avg_rentals_per_day
FROM fact_count_bikes fr
INNER JOIN dim_calendar dc ON fr.calendar_id = dc.dim_calendar_id
INNER JOIN dim_weather_category dw ON fr.weather_code = dw.weather_code
GROUP BY dw.weather_desc, day_type
ORDER BY dw.weather_desc, day_type;