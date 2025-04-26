DROP TABLE IF EXISTS mart_bike_rentals_working_vs_weekend_extended;
CREATE TABLE mart_bike_rentals_working_vs_weekend_extended AS
SELECT
    CASE WHEN dc.is_working_day THEN 'Working Day' ELSE 'Weekend / Holiday' END AS day_type,
    COUNT(DISTINCT TO_DATE(dc.year || '-' || LPAD(dc.month::text, 2, '0') || '-' || LPAD(dc.day::text, 2, '0'), 'YYYY-MM-DD')) AS total_days,
    SUM(fr.cnt_bike_no_registration + fr.cnt_bike_with_registration) AS total_rentals,
    ROUND(SUM(fr.cnt_bike_no_registration + fr.cnt_bike_with_registration) * 1.0 / 
          COUNT(DISTINCT TO_DATE(dc.year || '-' || LPAD(dc.month::text, 2, '0') || '-' || LPAD(dc.day::text, 2, '0'), 'YYYY-MM-DD')), 2) AS avg_rentals_per_day
FROM fact_count_bikes fr
INNER JOIN dim_calendar dc ON fr.calendar_id = dc.dim_calendar_id
GROUP BY day_type
ORDER BY day_type;