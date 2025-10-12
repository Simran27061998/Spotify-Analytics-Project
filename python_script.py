# %%
#Importing Pandas for data cleaning and manipulation

import pandas as pd

# %%
#Import raw data set

df = pd.read_csv('spotify_history_raw.csv')

# %%
#Checking first few rows

print(df.head())

# %%
# Check dataset info

df.info()

# %%
#Check the shape of the dataset

print(df.shape)

# %%
#Convert data type of timestamp column to datetime type

df['ts'] = pd.to_datetime(df['ts'],errors='coerce')

# %%
#Check Coversion

df.info()

# %%
#Check if any values failed to parse
 
failed = df['ts'].isna().sum()

print(failed)

# %%
#Extracting date and time components 

df['date'] = df['ts'].dt.date
df['time'] = df['ts'].dt.time
df['month'] = df['ts'].dt.month
df['year'] = df['ts'].dt.year
df['quater'] = df['ts'].dt.quarter
df['hour'] = df['ts'].dt.hour
df['day_name']= df['ts'].dt.day_name()



# %%
#create new column for weekend/weekday

df['type_of_day'] = df['day_name'].apply(
    lambda day: 'Weekend' if day in ['Saturday', 'Sunday'] else 'Weekday'
)

# %%
#create new column for time_of_the_day

import numpy as np

df['time_of_the_day'] = np.where(df['hour'].between(5,11),'Morning',
                        np.where(df['hour'].between(12,16),'Afternoon',
                        np.where(df['hour'].between(17,20),'Evening','Night')))

# %%
#Cleanup text columns

text_columns = ['artist_name','album_name','track_name','platform','reason_start','reason_end','shuffle','skipped'
                ,'day_name','type_of_day','time_of_the_day']

for col in text_columns:           # loop through all the columns you want to normalize
    if col in df.columns:          # only proceed if the column actually exists in the DataFrame.
        df[col] = df[col].fillna('unknown').astype(str).str.lower().str.strip().str.replace(' ',' ',regex=True) 

        # replace NaN
        # ensure text type
        # lowercase
        #remove leading/trailing spaces
        # collapse double spaces

# %%
#check for null values in columns

df.isnull().sum()

# %%
#Fill null values with 'unknown'

df['reason_start'] = df['reason_start'].fillna('unknown')
df['reason_end'] = df['reason_end'].fillna('unknown')

df.isnull().sum()

# %%
#Check how many rows have 0 ms_played

(df['ms_played'] == 0).sum()

# %%
#Remove rows having 0 ms_played and reset index to avoid gaps

df = df[df['ms_played'] > 0].reset_index(drop=True)

(df['ms_played'] == 0).sum()


# %%
#Check for duplicates

df.duplicated().sum()

# %%
#remove duplicates and reset the index

df= df.drop_duplicates().reset_index(drop=True)

df.duplicated().sum()

# %%
#Add mintues_played & hours_played columns

df['minutes_played'] = df['ms_played'] / 60000 
df['hours_played'] = df['minutes_played'] / 60
df

# %%
#Load csv file into mysql

from sqlalchemy import create_engine

# Replace with your own MySQL connection details
engine = create_engine("mysql+pymysql://root:27Simran$@localhost:3306/spotify_db")

# Export cleaned dataframe to a base table in MySQL
df.to_sql("spotify_raw", con=engine, if_exists="replace", index=False)


# %%
df_check = pd.read_sql('SELECT COUNT(*) AS row_count FROM spotify_raw', con=engine)
print(df_check['row_count'][0])

# %%
# Group by spotify_track_uri and count occurrences
duplicate_counts = df.groupby('spotify_track_uri').size()

# Filter only those that appear more than once
duplicate_counts = duplicate_counts[duplicate_counts > 1]

print(duplicate_counts)



# %%
import pandas as pd
from sqlalchemy import create_engine, text

# ----------------------------
# 1️⃣ Connect to MySQL
# ----------------------------
engine = create_engine("mysql+pymysql://root:27Simran$@localhost:3306/spotify_db")

# ----------------------------
# 2️⃣ Load cleaned raw data
# ----------------------------
df = pd.read_sql("SELECT * FROM spotify_raw", con=engine)

# ----------------------------
# 3️⃣ Load dimension tables
# ----------------------------
track_map = pd.read_sql("SELECT track_id, track_name, album_id FROM track_info", con=engine)
artist_map = pd.read_sql("SELECT artist_id, artist_name FROM artist_info", con=engine)
album_map = pd.read_sql("SELECT album_id, album_name, artist_id FROM album_info", con=engine)
platform_map = pd.read_sql("SELECT platform_id, platform_name FROM platform_info", con=engine)
date_map = pd.read_sql("SELECT date_id, full_date FROM date_info", con=engine)
time_map = pd.read_sql("SELECT time_id, full_time FROM time_info", con=engine)

# ----------------------------
# 4️⃣ Standardize text columns for clean matching
# ----------------------------
for col in ['track_name','album_name','artist_name','platform']:
    df[col + '_clean'] = df[col].str.lower().str.strip()

track_map['track_name_clean'] = track_map['track_name'].str.lower().str.strip()
album_map['album_name_clean'] = album_map['album_name'].str.lower().str.strip()
artist_map['artist_name_clean'] = artist_map['artist_name'].str.lower().str.strip()
platform_map['platform_name_clean'] = platform_map['platform_name'].str.lower().str.strip()

# ----------------------------
# 5️⃣ Create single key for track+album+artist
# ----------------------------
df['key'] = df['track_name_clean'] + '||' + df['album_name_clean'] + '||' + df['artist_name_clean']

track_album_artist_map = track_map.merge(album_map, on='album_id', how='left') \
                                  .merge(artist_map, on='artist_id', how='left')

track_album_artist_map['key'] = track_album_artist_map['track_name_clean'] + '||' + \
                                track_album_artist_map['album_name_clean'] + '||' + \
                                track_album_artist_map['artist_name_clean']

# ----------------------------
# 6️⃣ Merge IDs into raw data
# ----------------------------
df = df.merge(track_album_artist_map[['key','track_id','album_id','artist_id']], on='key', how='left')
df = df.merge(platform_map[['platform_id','platform_name_clean']], left_on='platform_clean', right_on='platform_name_clean', how='left')
df = df.merge(date_map[['date_id','full_date']], left_on='date', right_on='full_date', how='left')
df = df.merge(time_map[['time_id','full_time']], left_on='time', right_on='full_time', how='left')

# ----------------------------
# 7️⃣ Keep only required columns
# ----------------------------
df_fact = df[['track_id','artist_id','album_id','platform_id','date_id','time_id',
              'ms_played','minutes_played','hours_played','spotify_track_uri']]

# ----------------------------
# 8️⃣ Drop rows with missing IDs
# ----------------------------
missing = df_fact[df_fact[['track_id','artist_id','album_id','platform_id','date_id','time_id']].isna().any(axis=1)]
print("Rows with missing IDs:", len(missing))
if len(missing) > 0:
    df_fact = df_fact.dropna(subset=['track_id','artist_id','album_id','platform_id','date_id','time_id'])

df_fact = df_fact.reset_index(drop=True)

# ----------------------------
# 9️⃣ Insert into MySQL in chunks
# ----------------------------
chunk_size = 5000
# Use 'replace' for first run, then 'append' for subsequent runs
df_fact.to_sql('listening_history', con=engine, if_exists='replace', index=False)

# ----------------------------
# 10️⃣ Verify final row count
# ----------------------------
with engine.connect() as conn:
    result = conn.execute(text("SELECT COUNT(*) FROM listening_history"))
    print("Total rows in listening_history:", result.scalar())


# %%
import pandas as pd
from sqlalchemy import create_engine

# 1️⃣ Connect to MySQL
engine = create_engine("mysql+pymysql://root:27Simran$@localhost:3306/spotify_db")

# 2️⃣ List of dimension tables
dimension_tables = [
    'track_info',
    'album_info',
    'artist_info',
    'platform_info',
    'date_info',
    'time_info'
]

# 3️⃣ Loop through tables and check missing values
missing_summary = {}

for table in dimension_tables:
    df = pd.read_sql(f"SELECT * FROM {table}", con=engine)
    missing_counts = df.isna().sum()
    missing_summary[table] = missing_counts[missing_counts > 0]  # Only show columns with missing values

# 4️⃣ Display missing value summary
for table, missing in missing_summary.items():
    print(f"\nMissing values in {table}:")
    if missing.empty:
        print("✅ No missing values")
    else:
        print(missing)



