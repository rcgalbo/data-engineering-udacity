Background 
----------

> A startup called Sparkify wants to analyze the data they've been collecting on songs and user activity on their new music streaming app. The analytics team is particularly interested in understanding what songs users are listening to. Currently, they don't have an easy way to query their data, which resides in a directory of JSON logs on user activity on the app, as well as a directory with JSON metadata on the songs in their app.

deliverable: ETL code to create a Postgres database for analytic queries on Sparkify's song play data.


ETL Instructions
----------------

1. Run `create_tables.py` to create database and tables.
2. Run `etl.py` to load data into the database
3. Run `test.ipynb` to confirm the creation of the tables and verify the data is properly loaded.

Files
-----

- `data/` a directory containing the raw files to perform etl on.
- `create_tables.py` creates database, creates tables and drops the tables if they already exist.
- `etl.ipynb` contains the prototype solution of the etl process for a single file instance.
- `etl.py` contains the full ETL solution.
    - Parses raw files, inserts data into tables, iterates over all data input.
- `README.md` is a description of the project and it contents.
- `sql_queries.py` contains all of the queries to create and insert data into Postgres db. 
- `test.ipynb` is a notebook of tests to confim that the table have been properly created and data has inserted


Tables
------

List of tables created after ETL contains columns and the corresponding Postgres datatype (__Bolded__ represents primary key).

### fact table:

__songplays__ - records in log data associated with song plays i.e. records with page NextSong

| | |
| --- | --- |
| __songplay_id__  | varchar |
| start_time   | timestamp |
| user_id      | int |
| level        | varchar |
| song_id      | varchar |
| artist_id    | varchar |
| session_id   | int |
| location     | varchar |
| user_agent   | varchar |

### dimension tables:

__users__ - users in the app

|  |  |
| --- | --- |
| __user_id__      | int |
| first_name   | varchar |
| last_name    | varchar |
| gender       | varchar |
| level        | varchar |
        
__songs__ - songs in music database
    
| |  |
| --- | --- |
| __song_id__    |  varchar |
| title      |  varchar |
| artist_id  |  varchar |
| year       |  int |
| duration   |  numeric |
            
__artists__ - artists in music database

| |  |
| --- | --- |
| __artist_id__  |  varchar |
| name       |  varchar |
| location   |  varchar |
| latitude   |  numeric |
| longitude  |  numeric |

__time__ - timestamps of records in songplays broken down into specific units

| |  |
| --- | --- |
| __start_time__ | timestamp |
| hour       | int |
| day        | int |
| week       | int |
| month      | int |
| year       | int |
| weekday    | varchar |
    
    
Raw Data
--------

`song.json` file example:
```json
{"num_songs": 1, "artist_id": "AR8IEZO1187B99055E", "artist_latitude": null, "artist_longitude": null, "artist_location": "", "artist_name": "Marc Shaiman", "song_id": "SOINLJW12A8C13314C", "title": "City Slickers", "duration": 149.86404, "year": 2008}
```

`log.json` file example:
```json
{"artist":"Sydney Youngblood","auth":"Logged In","firstName":"Jacob","gender":"M","itemInSession":53,"lastName":"Klein","length":238.07955,"level":"paid","location":"Tampa-St. Petersburg-Clearwater, FL","method":"PUT","page":"NextSong","registration":1540558108796.0,"sessionId":954,"song":"Ain't No Sunshine","status":200,"ts":1543449657796,"userAgent":"\"Mozilla\/5.0 (Macintosh; Intel Mac OS X 10_9_4) AppleWebKit\/537.78.2 (KHTML, like Gecko) Version\/7.0.6 Safari\/537.78.2\"","userId":"73"}
```