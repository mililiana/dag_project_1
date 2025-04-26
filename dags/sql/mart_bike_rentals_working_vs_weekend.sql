DROP TABLE IF EXISTS mart_bike_rentals_working_vs_weekend;

CREATE TABLE mart_bike_rentals_working_vs_weekend AS
SELECT
    CASE WHEN dc.is_working_day THEN 'Working Day' ELSE 'Weekend / Holiday' END AS day_type,
    SUM(fr.cnt_bike_no_registration + fr.cnt_bike_with_registration) AS total_rentals
FROM fact_count_bikes fr
INNER JOIN dim_calendar dc ON fr.calendar_id = dc.dim_calendar_id
GROUP BY day_type
ORDER BY total_rentals DESC;
