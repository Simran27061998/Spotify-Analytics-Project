# Spotify-Analytics-Project
End-to-end Spotify listening analytics using Python, MySQL, and Power BI.

# Project Overview

This project analyzes 10+ years of Spotify streaming history (2013–2024) to uncover listening patterns, favorite artists, and platform usage. It demonstrates an end-to-end analytics workflow:

1.Python for data cleaning and preprocessing
2.MySQL for database modeling and SQL analysis
3.Power BI for dashboarding and business insights

The goal was to replicate a real-world analytics project and present results in both technical (SQL + data models) and business-friendly (visual dashboards) formats.

# Tools & Technologies

1.Python (Pandas, NumPy, SQLAlchemy) → cleaning, transformations
2.MySQL → relational schema, queries, analysis
3.Power BI → dashboarding, KPI visualization
4.GitHub → version control, portfolio presentation

# Repository Structure

spotify-analytics-project/
│
├── python_scripts/                 # Data cleaning script
│   └── spotify_history_cleaned_script.py
│
├── sql/                            # ERD and queries
│   ├── spotify_analysis_queries.md
│   └── erd_dbdiagram.png
│
├── sql_results/                    # Outputs of SQL queries
│   ├── q1_top_artists.csv
│   ├── q2_top_albums.csv
│   ├── q3_top_tracks.csv
│   └── ... up to q12
│
├── power_bi/                       # Power BI dashboard
│   └── Spotify_portfolio_project.pbix
│
└── README.md                       # Project documentation

# Data Cleaning (Python)

Steps performed in spotify_history_cleaned_script.py:

1.Parsed timestamps into date, time, year, quarter, etc.
2.Created derived features: weekday/weekend, time of day buckets.
3.Removed invalid rows (ms_played = 0) and duplicates.
4.Calculated duration in minutes and hours.
5.Exported cleaned dataset into MySQL and CSV for further analysis.

[spotify_history_cleaned_script.py](python_scripts/spotify_history_cleaned_script.py)

# Database Design (MySQL)

1. The project follows a Star Schema design:

a.Fact Table: listening_history (contains plays, durations, foreign keys)
b.Dimension Tables: artist_info, album_info, track_info, platform_info, date_info, time_info

2.Entity-Relationship Diagram (ERD):[ERD](sql/erd_dbdiagram.png)


# Business Questions Answered with SQL

1.Documented in spotify_analysis_queries.md.
2.Each query links to its CSV output in sql_results/.

# Key analyses include:

1.Top 3 artists, albums, and tracks per year
2.Artists appearing as #1 across multiple years
3.Yearly listening growth
4.Most-used platforms per year
5.Average listening session length by platform
6..Weekday vs weekend listening
7.Most active time of day
8.Top artist per platform
9.Most frequently played track (by count)
10.Highest listening quarter per year

[spotify_analysis_queries.md](sql/spotify_analysis_queries.md)

# Dashboard (Power BI)

Interactive dashboard built in Power BI:

1.KPIs: Total minutes, hours, unique tracks, albums, artists
2.Top 5 Artists/Albums/Tracks by minutes
3.Yearly & Monthly Listening Trends
4.Weekend vs Weekday breakdown
5.Heatmap: Listening hours vs days
6.Scatter plot: Avg minutes per play vs total plays

[Spotify_portfolio_project.pbix](power_bi/Spotify_portfolio_project.pbix)

# How to Reproduce

Clone the repo:

git clone https://github.com/<your-username>/spotify-analytics-project.git
cd spotify-analytics-project

1.Run the Python script to clean your Spotify export.
2.Load the cleaned data into MySQL using the schema.
3.Open the Power BI dashboard and connect it to the database or CSVs.

# Future Improvements

1.Automate ETL pipeline with Airflow or dbt
2.Deploy dashboard on Power BI Service or Tableau Public
3.Enrich with Spotify API metadata (genres, popularity)
4.Perform predictive modeling for listening trends

# Key Takeaways

End-to-end project: Python → SQL → Power BI

1.Strong focus on data modeling (Star Schema)
2.Showcased ability to answer business-style questions
3.Delivered a polished dashboard for stakeholders
