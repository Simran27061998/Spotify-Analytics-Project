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

```
## Query 2: Top 3 Albums by Total Listening Time Per Year.

```sql
SELECT year, album_name, total_minutes 
FROM (
    SELECT 
        date_info.year,
        album_info.album_name,
        ROUND(SUM(listening_history.minutes_played), 2) AS total_minutes,
        RANK() OVER(PARTITION BY date_info.year ORDER BY SUM(listening_history.minutes_played) DESC) AS row_no 
    FROM listening_history
    JOIN date_info ON listening_history.date_id = date_info.date_id
    JOIN album_info ON listening_history.album_id = album_info.album_id
    GROUP BY date_info.year, album_info.album_name
) ranked 
WHERE row_no <= 3
ORDER BY year;

```
## Query 3: Top 3 Tracks by Total Listening Time Per Year

```sql

SELECT year, track_name, total_minutes
FROM (
    SELECT 
        date_info.year, 
        track_info.track_name,
        ROUND(SUM(listening_history.minutes_played), 2) AS total_minutes,
        RANK() OVER(PARTITION BY date_info.year ORDER BY SUM(listening_history.minutes_played) DESC) AS row_no
    FROM listening_history
    JOIN date_info ON listening_history.date_id = date_info.date_id
    JOIN track_info ON listening_history.track_id = track_info.track_id
    GROUP BY date_info.year, track_info.track_name
) ranked
WHERE row_no <= 3 
ORDER BY year;

```

## Query 4: Artists Appearing as #1 Across Multiple Years

```sql

SELECT artist_name, COUNT(*) AS years_on_top
FROM (
    SELECT artist_info.artist_name,
           RANK() OVER(PARTITION BY date_info.year ORDER BY SUM(listening_history.minutes_played) DESC) AS row_no
    FROM listening_history
    JOIN artist_info  ON listening_history.artist_id = artist_info.artist_id
    JOIN date_info  ON listening_history.date_id = date_info.date_id
    GROUP BY date_info.year, artist_info.artist_name
) ranked 
WHERE row_no = 1
GROUP BY artist_name
ORDER BY years_on_top DESC;

```

## Query 5: Listening Growth Over the Years

```sql

SELECT date_info.year, ROUND(SUM(listening_history.minutes_played), 2) AS total_minutes
FROM listening_history 
JOIN date_info  ON listening_history.date_id = date_info.date_id
GROUP BY date_info.year
ORDER BY date_info.year;

```

## Query 6: Most-Used Platform Over the Years

```sql

SELECT year, platform_name, total_minutes
FROM (
    SELECT date_info.year,
           platform_info.platform_name,
           ROUND(SUM(listening_history.minutes_played),2) AS total_minutes,
           RANK() OVER(PARTITION BY date_info.year ORDER BY SUM(listening_history.minutes_played) DESC) AS row_no
    FROM listening_history
    JOIN platform_info  ON listening_history.platform_id = platform_info.platform_id
    JOIN date_info  ON listening_history.date_id = date_info.date_id
    GROUP BY date_info.year, platform_info.platform_name
) ranked 
WHERE row_no = 1
ORDER BY year;

```

## Query 7: Avg Minutes Per Session by Platform

```sql

SELECT 
    platform_info.platform_name,
    ROUND(AVG(listening_history.minutes_played), 2) AS avg_minutes_per_session
FROM listening_history 
JOIN platform_info  ON listening_history.platform_id = platform_info.platform_id
GROUP BY platform_info.platform_name
ORDER BY avg_minutes_per_session DESC;

```

## Query 8: Weekend vs Weekday Listening (Year by Year)

```sql

SELECT date_info.year, date_info.type_of_day,
       ROUND(SUM(listening_history.minutes_played),2) AS total_minutes
FROM listening_history
JOIN date_info ON listening_history.date_id = date_info.date_id
GROUP BY date_info.year, date_info.type_of_day
ORDER BY date_info.year, total_minutes DESC;

```

## Query 9: Most Active Listening Time of Day

```sql

SELECT time_info.time_of_the_day,
       ROUND(SUM(listening_history.minutes_played),2) AS total_minutes
FROM listening_history
JOIN time_info ON listening_history.time_id = time_info.time_id
GROUP BY time_info.time_of_the_day
ORDER BY total_minutes DESC;

```

## Query 10: Most Streamed Artist per Platform

```sql

SELECT platform_name, artist_name, total_minutes
FROM (
    SELECT platform_info.platform_name,
           artist_info.artist_name,
           ROUND(SUM(listening_history.minutes_played),2) AS total_minutes,
           RANK() OVER(PARTITION BY platform_info.platform_name ORDER BY SUM(listening_history.minutes_played) DESC ) AS row_no
    FROM listening_history
    JOIN platform_info  ON listening_history.platform_id = platform_info.platform_id
    JOIN artist_info  ON listening_history.artist_id = artist_info.artist_id
    GROUP BY platform_info.platform_name, artist_info.artist_name
) ranked
WHERE row_no = 1
ORDER BY total_minutes DESC;

```

## Query 11: Most Played Track (by Count)

```sql

SELECT artist_info.artist_name, track_info.track_name,
       COUNT(*)  AS play_count
FROM listening_history
JOIN track_info ON listening_history.track_id = track_info.track_id
JOIN artist_info  ON listening_history.artist_id = artist_info.artist_id
GROUP BY artist_info.artist_name, track_info.track_name
ORDER BY play_count DESC 
LIMIT 5;

```

## Query 12: Highest Listening Quarter Per Year

```sql

SELECT year, quarter, total_minutes
FROM (
    SELECT date_info.year,
           date_info.quarter,
           ROUND(SUM(listening_history.minutes_played), 2) AS total_minutes,
           RANK() OVER(PARTITION BY date_info.year ORDER BY SUM(listening_history.minutes_played) DESC) AS row_no
    FROM listening_history 
    JOIN date_info  ON listening_history.date_id = date_info.date_id
    GROUP BY date_info.year, date_info.quarter
) ranked 
WHERE row_no = 1
ORDER BY year;

