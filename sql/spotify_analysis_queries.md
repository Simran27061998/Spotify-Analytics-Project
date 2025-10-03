#  Spotify SQL Analysis

This file documents the **business questions**, their **SQL queries**, and **outputs**.

---

## Query 1: Top 3 Artists by Total Listening Time Per Year

```sql
SELECT year, artist_name, total_minutes
FROM (
    SELECT 
        date_info.year,
        artist_info.artist_name,
        ROUND(SUM(listening_history.minutes_played), 2) AS total_minutes,
        RANK() OVER(PARTITION BY date_info.year ORDER BY SUM(listening_history.minutes_played) DESC) AS row_no
    FROM listening_history 
    JOIN artist_info  ON listening_history.artist_id = artist_info.artist_id
    JOIN date_info  ON listening_history.date_id = date_info.date_id
    GROUP BY date_info.year, artist_info.artist_name
) ranked
WHERE row_no <= 3
ORDER BY year,total_minutes DESC;


