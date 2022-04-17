create database if not exists episodesdb;
use episodesdb;
create external table if not exists episode (
  rank int,
  show_name string,
  episode_name string,
  watchtime int,
  year_of_release int,
  episode_rating int,
  votes int,
  genre_1 string,
  genre_2 string,
  genre_3 string,
  episode_review string
)
row format delimited
fields terminated by ','
lines terminated by '\n'
stored as textfile location 'hdfs://namenode:8020/user/hive/data/episodesdb.db/episode';
