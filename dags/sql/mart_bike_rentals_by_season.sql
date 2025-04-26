DROP TABLE IF EXISTS mart_bike_rentals_by_season;
CREATE TABLE mart_bike_rentals_by_season AS
SELECT
    ds.season_desc, 
    SUM(fr.cnt_bike_no_registration) AS total_no_registration,  
    SUM(fr.cnt_bike_with_registration) AS total_with_registration 
FROM fact_count_bikes fr
INNER JOIN dim_season_category ds ON fr.season_code = ds.season_code
GROUP BY ds.season_desc
ORDER BY ds.season_desc;