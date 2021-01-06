import os.path
import pandas as pd
import requests
import json
import mysql.connector

NAME = 'DbMysql04'
HOST = 'mysqlsrv1.cs.tau.ac.il'
LOCAL = '127.0.0.1'

'''
helping methods
'''


def drop_tables(cursor):
    query = '''DROP TABLE movie_names'''
    cursor.execute(query)

    query = '''DROP TABLE actors'''
    cursor.execute(query)
    ctx.commit()
# creating tables


def create_tables(cursor):
    query = '''CREATE TABLE IF NOT EXISTS movie_names (
                id INT PRIMARY KEY, 
                f_title VARCHAR(100) NOT NULL, 
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
    query = '''INSERT INTO movie_names (
                    id, f_title, genre, duration, lang, budget, income) 
                    VALUES (%s, %s, %s, %s, %s, %s, %s)'''
    for index, row in df.iterrows():
        print(row['title'])
        query_params = row['imdb_title_id'], row['title'], row['genre'], row['duration'], \
                       row['language'], row['budget'], row['worlwide_gross_income']
        print('params: ', query_params)
        cursor.execute(query, query_params)  # // multi=False


# insert data to actors
def push_actor(cursor, name, id):
    pass


# insert data to movies
def push_movie(cursor, imdb_id, title):
    pass


'''
insert data to db
'''


def main(cursor):
    drop_tables(cursor)
    print("droped all tables")
    create_tables(cursor)
    print("done creating tables")
    push_csv(cursor)


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
