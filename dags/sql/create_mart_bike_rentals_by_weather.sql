DROP TABLE IF EXISTS mart_bike_rentals_by_weather;
CREATE TABLE mart_bike_rentals_by_weather AS
SELECT
    dc.year,                      
    dc.month,                     
    dw.weather_desc,            
    SUM(fr.cnt_bike_no_registration + fr.cnt_bike_with_registration) AS total_rentals
FROM fact_count_bikes fr
INNER JOIN dim_calendar dc ON fr.calendar_id = dc.dim_calendar_id
INNER JOIN dim_weather_category dw ON fr.weather_code = dw.weather_code
GROUP BY dc.year, dc.month, dw.weather_desc
ORDER BY dc.year, dc.month, dw.weather_desc;