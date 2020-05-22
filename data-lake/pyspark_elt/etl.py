import configparser
from datetime import datetime
import os
from pyspark.sql import SparkSession
from pyspark.sql.functions import udf, col, from_unixtime, monotonically_increasing_id
from pyspark.sql.functions import year, month, dayofmonth, hour, weekofyear, date_format
from pyspark.sql.types import StructType as R, StructField as Fld, DoubleType as Dbl, StringType as Str, IntegerType as Int, DateType as Dat, TimestampType

config = configparser.ConfigParser()
config.read('dl.cfg')

os.environ['AWS_ACCESS_KEY_ID']=config['AWS']['AWS_ACCESS_KEY_ID']
os.environ['AWS_SECRET_ACCESS_KEY']=config['AWS']['AWS_SECRET_ACCESS_KEY']


def create_spark_session():
    '''Create spark session object'''
    spark = SparkSession \
        .builder \
        .config("spark.jars.packages", "org.apache.hadoop:hadoop-aws:2.7.0") \
        .getOrCreate()
    return spark


def process_song_data(spark, input_data, output_data):
    '''Load input_data and extract song and artist table to output_data
    spark: spark session object
    input_data: path to s3 input bucket
    output_data: path to s3 output bucket
    returns: none
    '''
    # get filepath to song data file
    song_data = "{}song_data/*/*/*/*.json".format(input_data)
    
    # read song data file
    schema = R([
        Fld("artist_id",Str()),
        Fld("artist_latitude",Dbl()),
        Fld("artist_location",Str()),
        Fld("artist_longitude",Dbl()),
        Fld("artist_name",Str()),
        Fld("duration",Dbl()),
        Fld("num_songs",Int()),
        Fld("title",Str()),
        Fld("year",Int()),
    ])
    
    df = spark.read.json(song_data, schema = schema)

    # extract columns to create songs table
    songs = df.select(['title',
                       'artist_id',
                       'year',
                       'duration']).dropDuplicates()
    # create song id
    songs = songs.withColumn('song_id', monotonically_increasing_id())
    
    # write songs table to parquet files partitioned by year and artist
    print('---- writing songs table ----')
    songs_out = "{}songs/".format(output_data)
    songs.write.mode('overwrite').partitionBy('year','artist_id').parquet(songs_out)

    # extract columns to create artists table
    artists = df.select(['artist_id',
                         'artist_name',
                         'artist_location',
                         'artist_latitude',
                         'artist_longitude']).dropDuplicates()
    
    # write artists table to parquet files
    print('---- writing artists table ----')
    artist_out = "{}artists/".format(output_data)
    artists.write.mode('overwrite').parquet(artist_out)


def process_log_data(spark, input_data, output_data):
    '''Load input_data and extract remaining tables to output_data
    spark: spark session object
    input_data: path to s3 input bucket
    output_data: path to s3 output bucket
    returns: none
    '''
    # get filepath to log data file
    log_data = "{}log_data/*/*/*.json".format(input_data)

    # read log data file
    df = spark.read.json(log_data)
    
    # filter by actions for song plays
    df = df.filter(df.page == 'NextSong')

    # extract columns for users table    
    users = df.select(['userId','firstName','lastName','gender','level']).dropDuplicates()
    
    # write users table to parquet files
    print('---- writing users table ----')
    user_out = '{}users/'.format(output_data)
    users.write.mode('overwrite').parquet(user_out)

    # create timestamp column from original timestamp column
    df = df.withColumn('timestamp', from_unixtime(col('ts') / 1000))
    
    # extract columns to create time table
    times =  df.select("timestamp").dropDuplicates()
    times = times.withColumn("hour", hour(col("timestamp")))\
                .withColumn("day", dayofmonth(col("timestamp"))) \
                .withColumn("week", weekofyear(col("timestamp"))) \
                .withColumn("month", month(col("timestamp"))) \
                .withColumn("year", year(col("timestamp"))) \
                .withColumn("weekday", date_format(col("timestamp"), 'E'))

    # write time table to parquet files partitioned by year and month
    print('---- writing times table ---')
    time_out = '{}time/'.format(output_data)
    times.write.mode('overwrite').partitionBy('year','month').parquet(time_out)

    # read in song data to use for songplays table
    song_in = '{}songs/*/*/*'.format(output_data)
    song_df = spark.read.parquet(song_in)
    artist_in = '{}artists/*'.format(output_data)
    artist_df = spark.read.parquet(artist_in)
    
    song_log = df.join(song_df, (df.song == song_df.title))
    artist_song_log = song_log.join(artist_df, (song_log.artist == artist_df.artist_name))
    songplay = artist_song_log.join(times, ['timestamp'])

    # extract columns from joined song and log datasets to create songplays table 
    songplays = songplay.selectExpr('timestamp as start_time',
                                'userId as user_id',
                                'level',
                                'song_id',
                                'artist_id',
                                'sessionId as session_id',
                                'location',
                                'userAgent as user_agent')
    # create songplay id
    songplays = songplays.withColumn('songplay_id', monotonically_increasing_id())

    # write songplays table to parquet files partitioned by year and month
    print('---- writing songplays table ----')
    songplays_out='{}songplays/'.format(output_data)
    songplays.write.mode('overwrite').parquet(songplays_out)


def main():
    spark = create_spark_session()
    input_data = "s3a://udacity-dend/"
    output_data = config['AWS']['OUTPUT_BUCKET']
    
    process_song_data(spark, input_data, output_data)    
    process_log_data(spark, input_data, output_data)

if __name__ == "__main__":
    main()
