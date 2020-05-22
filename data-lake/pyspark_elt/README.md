Intro
=====

Task: ETL on data in S3 with Pyspark 

- Take data that is in S3
- Load proper data tables (listed below) in Pyspark
- Write these tables back to S3 bucket for future analysis

Instructions
------------

1. add aws keys to `dl.cfg` file
2. run `create_bucket.py` to generate the output S3 bucket if doesn't exist
3. make sure to update the `dl.cfg` with the `OUTPUT_BUCKET`
4. Setup EMR cluster to run job
5. `scp` both `etl.py` and `dl.cfg` to the master node
6. `ssh` into master node
7. make sure `pyspark` is installed on master node
    - if not run `sudo python3 -m pip install wheel && sudo python3 -m pip install pyspark`
8. On master node run `sudo spark-submit --deploy-mode client etl.py` to extract the tables and write to output S3 bucket

- [set python3 as default for spark](https://aws.amazon.com/premiumsupport/knowledge-center/emr-pyspark-python-3x/)
- [example of running pyspark on cluster with spark submit](https://aws.amazon.com/blogs/big-data/submitting-user-applications-with-spark-submit/)

Schema for Song Play Analysis
-----------------------------

### Fact Table

__songplays__ - records in log data associated with song plays i.e. records with page NextSong

songplay_id, start_time, user_id, level, song_id, artist_id, session_id, location, user_agent

### Dimension Tables

__users__ - users in the app:

user_id, first_name, last_name, gender, level

__songs__ - songs in music database:
        song_id, title, artist_id, year, duration
        
__artists__ - artists in music database:
        
artist_id, name, location, lattitude, longitude

__time__ - timestamps of records in songplays broken down into specific units:


start_time, hour, day, week, month, year, weekday

