import os.path
import numpy as np
import pandas as pd
import requests
import json
import mysql.connector
from Database import Database
from data_fill import *

NAME = 'DbMysql04'
HOST = 'mysqlsrv1.cs.tau.ac.il'
LOCAL = '127.0.0.1'
API_KEY = '7e759b2920f15726a47aecff3b17d4fb'


'''
helping methods
'''
db = Database()
db.connect()
# db.drop_table('movie')
db.drop_table('actors')
db.drop_table('movie_actor')
db.drop_table('movie_genre')
db.drop_table('movie_names')

db.create_movie_table()
db.create_actor_table()
db.create_movieActor_table()
db.create_movieGenre_table()

movies_df = filter_movies_csv()

def get_movies_from_api(movies_df):
    for index, row in movies_df.iterrows():
        findMovieRes = requests.get("https://api.themoviedb.org/3/find/{}?api_key={}&external_source=imdb_id".format(row['id'], API_KEY))
        if findMovieRes.status_code == 200:
            foundMovie = json.loads(findMovieRes.json())
            id = str(foundMovie['movie_results'][0].id)
            print("Got id from api: {}".format(id))
            movieDetailsRes = requests.get("https://api.themoviedb.org/3/movie/{}?api_key={}&language=en-US".format(id, API_KEY))
            if movieDetailsRes.status_code == 200:
                movieDetails = json.loads(movieDetailsRes.json())
                print("Got details")
                db.insert_movie((row['id'], movieDetails['original_title'], movieDetails['budget'], movieDetails['revenue'], \
                movieDetails['release_date'], movieDetails['poster_path'], movieDetails['overview'], row['rating']))
                print("Inserted into movie table")
                for genre in movieDetails['genres']:
                    db.insert_movie_genre((row['id'], genre['id']))
                    print("Inserted into movieGenre table")

get_movies_from_api(movies_df)
#
#
# def drop_tables(cursor):
#     query = '''DROP TABLE actors'''
#     cursor.execute(query)
#     query = '''DROP TABLE movie_actor'''
#     cursor.execute(query)
#     # query = '''DROP TABLE actors'''
#     # cursor.execute(query)
#     ctx.commit()
# creating tables
#
#
# def create_tables(cursor):
#     query = '''CREATE TABLE IF NOT EXISTS movie_names (
#                 id INT PRIMARY KEY,
#                 imbd_id VARCHAR(10) NOT NULL,
#                 movie_db_id INT,
#                 f_title VARCHAR(200) NOT NULL,
#                 genre VARCHAR(100),
#                 duration INT,
#                 lang VARCHAR(100),
#                 budget INT,
#                 income INT, year INT)'''
#     cursor.execute(query)
#
#     query = '''CREATE TABLE IF NOT EXISTS actors (
#                 id INT PRIMARY KEY,
#                 actor_name VARCHAR(100) NOT NULL,
#                 popularity DECIMAL (5,3))'''
#     cursor.execute(query)
#
#     query = '''CREATE TABLE IF NOT EXISTS genre(
#                 id INT PRIMARY KEY,
#                 genre_name VARCHAR(100) NOT NULL)'''
#     cursor.execute(query)
#
#     query = '''CREATE TABLE IF NOT EXISTS movie_genre (
#                 movie_id INT NOT NULL,
#                 genre_id INT NOT NULL)
#     '''
#     cursor.execute(query)
#
#     query = '''CREATE TABLE IF NOT EXISTS movie_actor(
#                 movie_id INT NOT NULL,
#                 actor_id INT NOT NULL)
#     '''
#
#     cursor.execute(query)
#
#     ctx.commit()
#
#
# # convert ids
# def imdb_id_to_id(imdb_id):
#     return int(imdb_id[2:])
#
#
# '''
# definitions on how to insert different data to DB
# '''
#
#
# # retrieve data form csv and insert
# def push_csv(cursor):
#     df = pd.read_csv('./APPLICATION-SOURCE-CODE/static/data/movies.csv')
#     df = df.replace({np.nan: None})  # remove nans
#     # insert budget and income from api
#     query = '''INSERT INTO movie_names (
#                     id, imbd_id, f_title, duration)
#                     VALUES (%s, %s, %s, %s)'''
#     for index, row in df.iterrows():
#         query_params = imdb_id_to_id(row['imdb_title_id']), row['imdb_title_id'], row['title'], row['duration']
#         # print("params:")
#         # print(query_params)
#         cursor.execute(query, query_params)  # // multi=False
#     ctx.commit()
#
#
# def push_actors_from_csv(cursor):
#     df = pd.read_csv('../names.csv')
#     df = df.replace({np.nan: None})
#     count = 0
#     count_rows = 123238
#     df.drop(df.index[:123238], inplace=True)
#     insert_actor_movie = '''INSERT INTO movie_actor (
#                         movie_id, actor_id)
#                          VALUES (%s, %s)'''
#     insert_actors = '''INSERT INTO actors (
#                         id, actor_name, popularity)
#                          VALUES (%s, %s, %s)'''
#     for index, row in df.iterrows():
#         if count < 100000:
#             imdb_name_id = row['imdb_name_id']
#             count_rows = count_rows+1
#             response = requests.get("https://api.themoviedb.org/3/find/" + str(imdb_name_id) +
#                                     "?api_key=" + API_KEY + "&external_source=imdb_id")
#             if response.status_code == 200:
#                 resp_json = response.json()
#                 if resp_json["person_results"]:
#                     actor_resp = resp_json["person_results"][0]
#                     actor_id = actor_resp['id']
#                     if 'popularity' in actor_resp:
#                         pop = actor_resp['popularity']
#                     else:
#                         pop = None
#                     actor_params = actor_id, actor_resp['name'], pop
#                     cursor.execute(insert_actors, actor_params)
#                     count = count+1
#                     print(count)
#                     response_movies = requests.get("https://api.themoviedb.org/3/person/" + str(actor_id)+
#                                                    "/movie_credits?api_key=" + API_KEY + "&language=en-US")
#                     if response_movies.status_code == 200:
#                         resp_json = response_movies.json()
#                         if resp_json["cast"]:
#                             cast_response = resp_json["cast"]
#                             for movie in cast_response:
#                                 # print(movie)
#                                 params = movie['id'], actor_id
#                                 cursor.execute(insert_actor_movie, params)
#             if count == 50000:
#                 print(count_rows)
#                 ctx.commit()
#         else:
#             break
#     print(count_rows)
#     ctx.commit()
#
#
# # insert data to actors
# def push_actor(cursor):
#     # first 30000
#     # actors = pd.read_csv('./APPLICATION-SOURCE-CODE/static/data/persons_ids_1.csv')
#     # actors_json = open('../person_ids_01_07_2021.json')
#     #  with open('../person_ids_01_07_2021.json') as actors_json:
#     #      actors = json.load(actors_json)
#     # actors = pd.read_json(actors_json)
#     actors = pd.read_json('../person_ids_01_07_2021.json', lines=True)
#     insert_actor_movie = '''INSERT INTO movie_actor (
#                     movie_id, actor_id)
#                      VALUES (%s, %s)'''
#     insert_actors = '''INSERT INTO actors (
#                     id, actor_name, popularity)
#                      VALUES (%s, %s, %s)'''
#     actors = actors.sort_values(by=['id'], ascending=True)
#     # delete first i*10000 rows
#     # actors = actors_.iloc[14536:]
#     actors.drop(actors.index[:88607], inplace=True)
#     print(actors.head())
#     count = 0
#     count_ids = 88607
#     for index, row in actors.iterrows():
#         if count < 20000:
#             person_id = row['id']
#             response = requests.get("https://api.themoviedb.org/3/person/"+str(person_id) +
#                                     "/movie_credits?api_key="+API_KEY+"&language=en-US")
#             count_ids = count_ids+1
#             if response.status_code == 200:
#                 resp_json = response.json()
#                 if resp_json["cast"]:
#                     # print("resp_json:")
#                     # print(resp_json["cast"][0])
#                     query_params = person_id, row['name'], row['popularity']
#                     cursor.execute(insert_actors, query_params)
#                     count = count + 1
#                     print(count)
#                     cast_response = resp_json["cast"]
#                     # print("cast_response:")
#                     # print(cast_response)
#                     for movie in cast_response:
#                         # print(movie)
#                         params = movie['id'], person_id
#                         cursor.execute(insert_actor_movie, params)
#         else:
#             break
#     print(count_ids)
#     ctx.commit()
#
#
# # insert data to movies from api
# def push_movie(cursor):
#     df = pd.read_csv('./APPLICATION-SOURCE-CODE/static/data/movies.csv')
#     df = df.replace({np.nan: None})
#     count = 0
#     update_query = '''UPDATE movie_names
#                     SET movie_db_id = %s, lang = %s
#                     WHERE id = %s'''
#     insert_query = '''INSERT INTO movie_genre (
#                     movie_id, genre_id)
#                      VALUES (%s, %s)'''
#
#     for index, row in df.iterrows():
#         imdb_id = row['imdb_title_id']
#         id = imdb_id_to_id(imdb_id)
#         response = requests.get("https://api.themoviedb.org/3/find/"+imdb_id +
#                                "?api_key="+API_KEY+"&external_source=imdb_id")
#         if response.status_code == 200:
#             resp_json = response.json()
#             if resp_json["movie_results"]:
#                 movie_resp = resp_json["movie_results"][0]
#                 query_params = movie_resp['id'], movie_resp['original_language'], id
#                 print(query_params)
#                 cursor.execute(update_query, query_params)
#                 count = count+1
#                 for gen in movie_resp['genre_ids']:
#                     params = id, gen
#                     cursor.execute(insert_query, params)
#     print(count)
#     ctx.commit()
#
#
# # insert genres into table from api
# def get_genres(cursor):
#     genres = requests.get('https://api.themoviedb.org/3/genre/movie/list?api_key=7e759b2920f15726a47aecff3b17d4fb')
#     genres_dict = genres.json()
#     query = '''INSERT INTO genre(
#                 id, genre_name)
#                 VALUES (%s, %s)'''
#     for gen in genres_dict['genres']:
#         query_params = gen['id'], gen['name']
#         cursor.execute(query, query_params)
#         print("params:")
#         print(query_params)
#     ctx.commit()
#
#
# '''
# insert data to db
# '''
#
#
# def main(cursor):
#     # drop_tables(cursor)
#     # print("droped tables")
#     # print("creating tables")
#     # create_tables(cursor)
#     # print("done creating tables")
#     # get_genres(cursor)
#     # push_csv(cursor)
#     # push_actor(cursor)
#     push_actors_from_csv(cursor)
#     print("done_pushing_actors")
#
#
# '''
# connection to server details
# '''
#
# # print("connecting to mysql")
# # ctx = mysql.connector.connect(user=NAME, password=NAME, host=HOST, database=NAME)
# # cursor = ctx.cursor()
#
# # main(cursor)
#
# # cursor.close()
# # ctx.close()
#
# def insert_csv(db):
#     df = pd.read_csv('./APPLICATION-SOURCE-CODE/static/data/movies.csv', usecols=['imdb_title_id', 'title'])
#     print(df.head())
#
#     for index, row in enumerate(df.to_numpy()):
#         if index < 5_000:
#             if index % 1_000 == 0:
#                 print('done ', index)
#                 print(tuple(row))
#             db.insert_movie(tuple(row))
#         else:
#             break
#
# db = Database()
# db.connect()
#
# # db.drop_movie_table()
# # db.create_movie_table()
# # insert_csv(db)
# movies = db.search_movie('Fi')
# print(movies)
# query = ''' select  title
#             from    movie
#             limit   15     '''
# print(db.execute_query(query))
#
# db.disconnect()
#
# '''
# API retrieve
# '''
#
# # with open('./APPLICATION-SOURCE-CODE/static/data/person_ids_01_04_2021.json') as json_file:
# #     data = json.load(json_file)
# #     for item in data:
# #         print(item)
# #
# # source_url = '';
# # get_movies = requests.get(source_url)
# # if get_movies.status_code == 200:
# #     json_movies = get_movies.json()
# #
#
# # result = requests.get('https://api.themoviedb.org/3/movie/550?api_key=7e759b2920f15726a47aecff3b17d4fb')
# # result_dict = result.json()
# # print(result_dict['id'])
#
#
#
# def filter_movies_csv():
#     df = pd.read_csv('./APPLICATION-SOURCE-CODE/static/data/ratings.csv', usecols=['imdb_title_id', 'weighted_average_vote'])
#     df.rename(columns={'imdb_title_id': 'id', 'weighted_average_vote': 'rating'}, inplace=True)
#     return df.nlargest(10_000, 'rating')
#
#
# def filter_actors_csv(movies_df):
#     df = pd.read_csv('./APPLICATION-SOURCE-CODE/static/data/movie_actors.csv', usecols=['imdb_title_id', 'imdb_name_id', 'category'])
#     df.rename(columns={'imdb_title_id': 'movie_id', 'imdb_name_id': 'actor_id'}, inplace=True)
#     movies_df.rename(columns={'id' : 'movie_id'})
#     df.merge(movies_df, how='inner', on='movie_id')
#     df = df.iloc(df['category'] == 'actress' | df['category'] == 'actor')
#     df = df['actor_id']
#     return df.drop_duplicates('actor_id')
#
#
# def filter_movieActors_csv():
#     pass
#
#
