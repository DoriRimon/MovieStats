import os.path
import pandas as pd
import requests
import json
import mysql.connector
import numpy as np

NAME = 'DbMysql04'
HOST = 'mysqlsrv1.cs.tau.ac.il'
LOCAL = '127.0.0.1'
API_KEY = '7e759b2920f15726a47aecff3b17d4fb'
'''
helping methods
'''


def drop_tables(cursor):
    query = '''DROP TABLE movie_names'''
    # cursor.execute(query)

    # query = '''DROP TABLE actors'''
    # cursor.execute(query)
    # ctx.commit()
# creating tables


def create_tables(cursor):
    query = '''CREATE TABLE IF NOT EXISTS movie_names (
                id INT PRIMARY KEY, 
                imbd_id VARCHAR(10) NOT NULL,
                movie_db_id INT,
                f_title VARCHAR(200) NOT NULL, 
                genre VARCHAR(100),
                duration INT, 
                lang VARCHAR(100), 
                budget INT, 
                income INT, year INT)'''
    cursor.execute(query)

    query = '''CREATE TABLE IF NOT EXISTS actors (
                id INT PRIMARY KEY,
                actor_name VARCHAR(100) NOT NULL)'''
    cursor.execute(query)

    query = '''CREATE TABLE IF NOT EXISTS genre(
                id INT PRIMARY KEY,
                genre_name VARCHAR(100) NOT NULL)'''
    cursor.execute(query)

    query = '''CREATE TABLE IF NOT EXISTS movie_genre (
                movie_id INT NOT NULL,
                genre_id INT NOT NULL)
    '''
    cursor.execute(query)

    ctx.commit()


# convert ids
def imdb_id_to_id(imdb_id):
    return int(imdb_id[2:])


'''
definitions on how to insert different data to DB
'''


# retrieve data form csv and insert
def push_csv(cursor):
    df = pd.read_csv('./APPLICATION-SOURCE-CODE/static/data/movies.csv')
    df = df.replace({np.nan: None})  # remove nans
    # insert budget and income from api
    query = '''INSERT INTO movie_names (
                    id, imbd_id, f_title, duration) 
                    VALUES (%s, %s, %s, %s)'''
    for index, row in df.iterrows():
        query_params = imdb_id_to_id(row['imdb_title_id']), row['imdb_title_id'], row['title'], row['duration']
        # print("params:")
        # print(query_params)
        cursor.execute(query, query_params)  # // multi=False
    ctx.commit()


# insert data to actors
def push_actor(cursor, name, id):
    pass


# insert data to movies from api
def push_movie(cursor):
    df = pd.read_csv('./APPLICATION-SOURCE-CODE/static/data/movies.csv')
    df = df.replace({np.nan: None})
    update_query = '''UPDATE movie_names 
                    SET movie_db_id = %s, lang = %s
                    WHERE id = %s'''
    insert_query = '''INSERT INTO movie_genre (
                    movie_id, genre_id)
                     VALUES (%s, %s)'''
    for index, row in df.iterrows():
        imdb_id = row['imdb_title_id']
        id = imdb_id_to_id(imdb_id)
        response = requests.get("https://api.themoviedb.org/3/find/"+imdb_id +
                                "?api_key="+API_KEY+"&external_source=imdb_id")
        if response.status_code == 200:
            print('status 200')
            resp_json = response.json()
            print('converted to jason')
            movie_resp = resp_json["movie_results"]
            print("movie response:")
            print(movie_resp)
            print(movie_resp['adult'])
            print(movie_resp['id'], movie_resp['original_language'], id)
            query_params = movie_resp['id'], movie_resp['original_language'], id
            cursor.execute(update_query, query_params)
            for gen in movie_resp['genre_ids']:
                params = imdb_id_to_id(row['imdb_title_id']), gen
                cursor.execute(insert_query, params)

    ctx.commit()


# insert genres into table from api
def get_genres(cursor):
    genres = requests.get('https://api.themoviedb.org/3/genre/movie/list?api_key=7e759b2920f15726a47aecff3b17d4fb')
    genres_dict = genres.json()
    query = '''INSERT INTO genre(
                id, genre_name) 
                VALUES (%s, %s)'''
    for gen in genres_dict['genres']:
        query_params = gen['id'], gen['name']
        cursor.execute(query, query_params)
        print("params:")
        print(query_params)
    ctx.commit()

'''
insert data to db
'''


def main(cursor):

    # drop_tables(cursor)
    # print("droped all tables")
    print("creating tables")
    create_tables(cursor)
    # print("done creating tables")
    # get_genres(cursor)
    # push_csv(cursor)
    push_movie(cursor)
    print("done_pushing_movie")


'''
connection to server details
'''
print("connecting to mysql")
ctx = mysql.connector.connect(user=NAME, password=NAME, host=HOST, database=NAME)
cursor = ctx.cursor()

main(cursor)

cursor.close()
ctx.close()

'''
API retrieve
'''

# with open('./APPLICATION-SOURCE-CODE/static/data/person_ids_01_04_2021.json') as json_file:
#     data = json.load(json_file)
#     for item in data:
#         print(item)
#
# source_url = '';
# get_movies = requests.get(source_url)
# if get_movies.status_code == 200:
#     json_movies = get_movies.json()
#

result = requests.get('https://api.themoviedb.org/3/movie/550?api_key=7e759b2920f15726a47aecff3b17d4fb')
result_dict = result.json()
print(result_dict['id'])
