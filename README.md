## Project background
Startup company Sparkify needs to analyze the data they collected on songs and user activities on their new music streaming app. Data files are in JSON format and will need to be extracted and loaded into a modeled database for analyze. Sparkify’s analytical goal is to understand what songs users are listening to. This project is to help Sparkify to achieve their analytical goal.


## Project implementation description
The project implementation includes two key components. 

The first component is to design and model the database tables to store the data. The model should be effective to answer questions such as what song a user listened to in last month. Star schema structure is designed to make the queries more effective. 
- We used postgresql database. There are one Fact table (songplays) and four Dimension tables (users, songs, artists, time). More details can be found in "Table structures" section.
- Table drop and creation sql statements are in sql_queries.py script.
- create_tables.py create a postgresql database and calls sql_queries.py to do actual table drop and creation. 

The second component is to design an ETL pipeline which will extract data from JSON file and after some transformations load data into database tables.
ETL pipeline code is in etl.py file. This script builds three functions. 
- Function process_song_file() extracts data from files in “data/song_data” and load data into songs table and artists table. 
- Function process_log_file() extracts data from files in “data/log_data” and load data into time table, users table and songplays table. 
- Function process_data() gets file path and name information of all files in a given directory. Then uses loop to call process functions(process_song_file or process_log_file in this project) to process all files in the given directory.

## Table structures
- Fact Table
  - songplays - records in log data associated with song plays i.e. records with page NextSong
    songplay_id, start_time, user_id, level, song_id, artist_id, session_id, location, user_agent
    In songplays table the primary key is songplay_id. This is an auto generated value using postgresql "serial" data type to guarantee no duplicate values.
- Dimension Tables
  - users - users in the app
    user_id, first_name, last_name, gender, level
    In users table the primary key is user_id. user_id is loaded from log files and can be used to identify a unique user.
  - songs - songs in music database
    song_id, title, artist_id, year, duration
    In songs table the primary key is song_id. song_id is loaded from log files and can be used to identify a song.
  - artists - artists in music database
    artist_id, name, location, latitude, longitude
    In artists table the primary key is artist_id. artist_id is loaded from log files and can be used to identify a unique artist.
  - time - timestamps of records in songplays broken down into specific units
    start_time, hour, day, week, month, year, weekday
    In time table there is no primary key since song start time can be same. However the start_time should always have a value. So start_time has a "NOT NULL" constraint.
- Star schema join relationships between tables
  - users table can be joined to songplays table on user_id
  - songs table can be joined to songplays table on song_id
  - artist table can be joined to songplays table on artist_id
  - time table can be joined to songplays table on start_time
 

## How to run the scripts
1. In a terminal window where python is installed run “python create_tables.py” to create postgresql database and reset tables.
2. In the same terminal window run “python etl.py” to process and load data into tables.

## Example queries
Question: what songs were people listening to in November 2018?
SELECT songs.title as songtitle 
FROM songplays,time,songs 
where songplays.start_Time=time.start_time and time.year=2018 and time.month=11 and songplays.song_id=songs.song_id and songplays.song_id!='None';

## Files in the submission
- sql_queries.py: This script has tables drop and creation sql statements, as well as insert and select statements which will populate the tables.
- create_tables.py: This script creates a postgresql database and calls sql_queries.py to do actual table drop and creation.
- etl.py: This script reads and processes files from song_data and log_data and loads them into tables.
- etl.ipynb: This file reads and processes a single file from song_data and log_data and loads the data into tables. 
- test.ipynb: This file displays the first few rows of each table to let me check database.
- README.md: This file provides discussion on my project.