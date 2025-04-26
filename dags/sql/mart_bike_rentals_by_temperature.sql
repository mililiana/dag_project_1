DROP TABLE IF EXISTS mart_bike_rentals_by_temperature;
CREATE TABLE mart_bike_rentals_by_temperature AS
SELECT
    dt.temp_category,
    SUM(fr.cnt_bike_no_registration + fr.cnt_bike_with_registration) AS total_rentals
FROM fact_count_bikes fr
INNER JOIN dim_temp_category dt ON fr.temp_category_id = dt.category_id
GROUP BY 1
ORDER BY total_rentals DESC;