import configparser
from create_cluster import create_session, fetch_arn

# CONFIG
config = configparser.ConfigParser()
config.read('dwh.cfg')
session = create_session(config['AWS']['KEY'],config['AWS']['SECRET'])

ARN = fetch_arn(session, config)
LOG_DATA = config['S3']['LOG_DATA']
LOG_JSONPATH = config['S3']['LOG_JSONPATH']
SONG_DATA = config['S3']['SONG_DATA']


# DROP TABLES

staging_events_table_drop = "drop table if exists staging_events"
staging_songs_table_drop = "drop table if exists staging_songs"
songplay_table_drop = "drop table if exists songplays"
user_table_drop = "drop table if exists users"
song_table_drop = "drop table if exists songs"
artist_table_drop = "drop table if exists artists"
time_table_drop = "drop table if exists time"

# CREATE TABLES

staging_events_table_create= ("""
CREATE TABLE IF NOT EXISTS staging_events (
    artist          text,
    auth            text,
    firstName       text,
    gender          text,
    itemInSession   int,
    lastName        text,
    length          numeric,
    level           text,
    location        text,
    method          text,
    page            text,
    registration    numeric,
    sessionId       int,
    song            text,
    status          int,
    ts              timestamp,
    userAgent       text,
    userId          int
)
""")

staging_songs_table_create = ("""
create table if not exists staging_songs (
    num_songs        int ,
    artist_id        text,
    artist_latitude  numeric,
    artist_longitude numeric,
    artist_location  text,
    artist_name      text,
    song_id          text,
    title            text,
    duration         numeric,
    year             int
)
""")

songplay_table_create = ("""
CREATE TABLE IF NOT EXISTS songplays (
    songplay_id int IDENTITY(0,1) PRIMARY KEY,
    start_time  timestamp not null SORTKEY DISTKEY,
    user_id     int not null,
    level       text,
    song_id     text not null,
    artist_id   text not null,
    session_id  int,
    location    text,
    user_agent  text
)
""")

user_table_create = ("""
CREATE TABLE IF NOT EXISTS users (
    user_id      int primary key sortkey,
    first_name   text not null,
    last_name    text not null,
    gender       text,
    level        text
)
""")

song_table_create = ("""
CREATE TABLE IF NOT EXISTS songs (    
    song_id   text primary key,
    title     text,
    artist_id text not null,
    year      int not null,
    duration  numeric
)
""")

artist_table_create = ("""
create table if not exists artists (
    artist_id  text primary key,
    name       text,
    location   text,
    latitude   numeric,
    longitude  numeric
)
""")

time_table_create = ("""
create table if not exists time (
    start_time timestamp not null distkey sortkey, 
    hour       int, 
    day        int, 
    week       int, 
    month      int, 
    year       int, 
    weekday    varchar
)
""")

# STAGING TABLES

staging_events_copy = (f"""
    copy staging_events 
    from {LOG_DATA}
    iam_role '{ARN}'
    format as json {LOG_JSONPATH}
    region 'us-west-2'
    timeformat as 'epochmillisecs'
""")

staging_songs_copy = (f"""
    copy staging_songs 
    from {SONG_DATA}
    iam_role '{ARN}'
    json 'auto'
    region 'us-west-2'
""")

# FINAL TABLES

user_table_insert = ("""
    insert into users (user_id, first_name, last_name, gender, level)
    select  distinct(userId)    AS user_id,
            firstName           AS first_name,
            lastName            AS last_name,
            gender,
            level
    from staging_events
    where page = 'NextSong'
    and user_id is not Null
""")

song_table_insert = ("""
    insert into songs (song_id, title, artist_id, year, duration)
    select distinct(song_id) as song_id,
            title,
            artist_id,
            year,
            duration
    from staging_songs
    where song_id is not Null
""")

artist_table_insert = ("""
    insert into artists (artist_id, name, location, latitude, longitude)
    select distinct(artist_id)  as artist_id,
            artist_name         as name,
            artist_location     as location,
            artist_latitude     as latitude,
            artist_longitude    as longitude
    from staging_songs
    where artist_id is not Null
""")

time_table_insert = ("""
    insert into time (start_time, hour, day, week, month, year, weekday)
    select distinct(start_time)            as start_time,
            extract(hour from start_time)  as hour,
            extract(day from start_time)   as day,
            extract(week from start_time)  as week,
            extract(month from start_time) as month,
            extract(year from start_time)  as year,
            extract(dayofweek from start_time) as weekday
    from songplays
""")

songplay_table_insert = ("""
    insert into songplays (start_time, user_id, level, song_id, 
                            artist_id, session_id, location, user_agent)
    select distinct(se.ts) as start_time,
            se.userId     as user_id,
            se.level       as level,
            ss.song_id     as song_id,
            ss.artist_id   as artist_id,
            se.sessionId   as session_id,
            se.location    as location,
            se.userAgent   as user_agent
    from staging_events as se
    join staging_songs as ss ON (se.song = ss.title AND se.artist= ss.artist_name)
    where se.page = 'NextSong'
""")


# QUERY LISTS

create_table_queries = [staging_events_table_create, staging_songs_table_create, songplay_table_create, user_table_create, song_table_create, artist_table_create, time_table_create]
drop_table_queries = [staging_events_table_drop, staging_songs_table_drop, songplay_table_drop, user_table_drop, song_table_drop, artist_table_drop, time_table_drop]
copy_table_queries = [staging_events_copy, staging_songs_copy]
insert_table_queries = [songplay_table_insert, user_table_insert, song_table_insert, artist_table_insert, time_table_insert]
