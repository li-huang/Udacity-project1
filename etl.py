import os
import glob
import psycopg2
import pandas as pd
from sql_queries import *


def process_song_file(cur, filepath):
    """
    The function to process song files and load data into songs table and artists table. 
  
        Parameters: 
            cur: The cursor of the given database
            filepath: The path and file name of the song file
          
        Returns: 
            None.
    """
    # open song file
    df = pd.read_json(filepath,typ='series')

    # insert song record
    song_data = df.loc[['song_id','title','artist_id','year','duration']].values.tolist()
    cur.execute(song_table_insert, song_data)
    
    # insert artist record
    artist_data = artist_data = df.loc[['artist_id','artist_name','artist_location','artist_latitude','artist_longitude']].values.tolist()
    cur.execute(artist_table_insert, artist_data)


def process_log_file(cur, filepath):
    """
    The function to process log files and load data into time table,users table and songplays table. 
  
        Parameters: 
            cur: The cursor of the given database
            filepath: The path and file name of the log file
          
        Returns: 
            None.
    """
    # open log file
    df = pd.read_json(filepath,lines=True)

    # filter by NextSong action
    df =  df[df['page']=="NextSong"]

    # convert timestamp column to datetime
    t = pd.to_datetime(df['ts'],unit='ms')
    
    # insert time data records
    time_data = [df['ts'].values.tolist(),t.dt.hour.values.tolist(),t.dt.day.values.tolist(),t.dt.week.values.tolist(),t.dt.month.values.tolist(),t.dt.year.values.tolist(),t.dt.dayofweek.values.tolist()]
    column_labels = ["ts","hour","day","week","month","year","weekday"]
    time_df = pd.DataFrame(dict(zip(column_labels,time_data)))

    for i, row in time_df.iterrows():
        cur.execute(time_table_insert, list(row))

    # load user table
    user_df = df[['userId','firstName','lastName','gender','level']]

    # insert user records
    for i, row in user_df.iterrows():
        cur.execute(user_table_insert, list(row))

    # insert songplay records
    for index, row in df.iterrows():
        
        # get songid and artistid from song and artist tables
        cur.execute(song_select, (row.song, row.artist, row.length))
        results = cur.fetchone()
        
        if results:
            songid, artistid = results
        else:
            songid, artistid = None, None

        # insert songplay record
        songplay_data = (row.ts,row.userId,row.level,songid,artistid,row.sessionId,row.location,row.userAgent)
        cur.execute(songplay_table_insert, songplay_data)


def process_data(cur, conn, filepath, func):
    """
    The function to iterate over files in a given directory and call process data functions to process and load data into tables. 
  
        Parameters: 
            cur: The cursor of the given database
            conn: The connection to a given database
            filepath: The parent directory of files
            func: The function name which will process the data files
          
        Returns: 
            None.
    """
    # get all files matching extension from directory
    all_files = []
    for root, dirs, files in os.walk(filepath):
        files = glob.glob(os.path.join(root,'*.json'))
        for f in files :
            all_files.append(os.path.abspath(f))

    # get total number of files found
    num_files = len(all_files)
    print('{} files found in {}'.format(num_files, filepath))

    # iterate over files and process
    for i, datafile in enumerate(all_files, 1):
        func(cur, datafile)
        conn.commit()
        print('{}/{} files processed.'.format(i, num_files))


def main():
    """The main function to process all song files and load files and load data into songs table,artists table,time table, users table and songplays table."""
    conn = psycopg2.connect("host=127.0.0.1 dbname=sparkifydb user=student password=student")
    cur = conn.cursor()

    process_data(cur, conn, filepath='data/song_data', func=process_song_file)
    process_data(cur, conn, filepath='data/log_data', func=process_log_file)

    conn.close()


if __name__ == "__main__":
    main()