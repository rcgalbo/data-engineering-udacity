Background
----------
This project runs end-to-end ETL process on AWS loading data from s3 buckets into a redshift database.


Instructions
------------

1. fill out `dwh.cfg` with aws key information as well as redshift cluster information
2. run `create_cluster.py` to configure a redshift cluster
    - must be setup in aws region `us-west-2` so that it will be able to access data in the udemy s3 bucket
3. run `create_tables.py` to create the staging & db tables
4. run `etl.py` to load the data into the staging & db tables
5. when the cluster is no longer needed run `delete_cluster.py` to delete the cluster and its configuration

To test that the data is properly loaded into the redshift cluster evaluate the code in the notebook `test_sql.ipynb`.

These instructions are included step-by-step in the `run_etl.ipynb` notebook.

Staging DB
----------

`songs.json` for staging_songs:
```json
{"num_songs": 1, "artist_id": "ARJIE2Y1187B994AB7", "artist_latitude": null, "artist_longitude": null, "artist_location": "", "artist_name": "Line Renaud", "song_id": "SOUPIRU12A6D4FA1E1", "title": "Der Kleine Dompfaff", "duration": 152.92036, "year": 0}
```

staging_songs - staging table for songs data
___name_  _data_type___
- num_songs int 
- artist_id text
- artist_latitude numeric
- artist_longitude numeric
- artist_location text
- artist_name text
- song_id text
- title text
- duration numeric
- year int

bucket: `s3://udacity-dend/song_data`

directory structure:
```
song_data/A/B/C/TRABCEI128F424C983.json
song_data/A/A/B/TRAABJL12903CDCF1A.json
```


`events.json` for staging_events:
```json
{"artist":"Sydney Youngblood","auth":"Logged In","firstName":"Jacob","gender":"M","itemInSession":53,"lastName":"Klein","length":238.07955,"level":"paid","location":"Tampa-St. Petersburg-Clearwater, FL","method":"PUT","page":"NextSong","registration":1540558108796.0,"sessionId":954,"song":"Ain't No Sunshine","status":200,"ts":1543449657796,"userAgent":"\"Mozilla\/5.0 (Macintosh; Intel Mac OS X 10_9_4) AppleWebKit\/537.78.2 (KHTML, like Gecko) Version\/7.0.6 Safari\/537.78.2\"","userId":"73"}
```

staging_events - staging table for events data

___name_  _data_type___
- artist text
- auth text
- firstName text
- gender text
- itemInSession int
- lastName text
- length numeric
- level text
- location text
- method text
- page text
- registration numeric
- sessionId int
- song text
- status int
- ts timestamp
- userAgent text
- userId int

bucket: `s3://udacity-dend/log_data`

directory structure:
```
log_data/2018/11/2018-11-12-events.json
log_data/2018/11/2018-11-13-events.json
```


Final DB
--------

### Fact Table

__songplays__ - records in event data associated with song plays i.e. records with page NextSong

___name_  _data_type___
- songplay_id int primary key,
- start_time  timestamp not null sortkey distkey,
- user_id     int not null,
- level       text,
- song_id     text not null,
- artist_id   text not null,
- session_id  int,
- location    text,
- user_agent  text

### Dimension Tables

__users__ - users in the app

___name_  _data_type___
- user_id      int primary key sortkey,
- first_name   text not null,
- last_name    text not null,
- gender       text,
- level        text,
    
__songs__ - songs in music database

___name_  _data_type___
- song_id   text primary key,
- title     text,
- artist_id text not null,
- year      int not null,
- duration  numeric
    
__artists__ - artists in music database
        
___name_  _data_type___
- artist_id  text primary key,
- name       text,
- location   text,
- latitude   numeric,
- longitude  numeric

__time__ - timestamps of records in songplays broken down into specific units

___name_  _data_type___
- start_time timestamp not null distkey sortkey,
- hour int, 
- day int, 
- week int, 
- month int, 
- year int, 
- weekday varchar
