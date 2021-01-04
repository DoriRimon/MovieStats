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


# creating tables
def create_tables(cursor):
    query = '''CREATE TABLE IF NOT EXISTS movie_names (id INT PRIMARY KEY, title VARCHAR(100) NOT NULL, genre VARCHAR(100),' \
            ' duration INT, language VARCHAR(100), budget INT, income INT, year INT)'''
    cursor.execute(query)

    query = '''CREATE TABLE IF NOT EXISTS actors (id INT PRIMARY KEY, name VARCHAR(100) NOT NULL)'''
    cursor.execute(query)


# convert ids
def imdb_id_to_id(imdb_id):
    return int(imdb_id[2:])


'''
definitions on how to insert different data to DB
'''


# retrieve data form csv and insert
def push_csv(curosr):
    df = pd.read_csv('./APPLICATION-SOURCE-CODE/static/data/movies.csv')
    for index, row in df.iterrows():
        query_params = imdb_id_to_id(row['imdb_title_id']), row['title'], row['genre'], row['duration'], row['budget'],\
                       row['worlwide_gross_income']
        # print('params: ', query_params)
        query = '''insert into movie_names (id, title, genre, duration, budget, income) values (%s, %s, %s, %s, %s, %s)'''
        cursor.execute(query, query_params, multi=False) 


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
    create_tables(cursor)
    push_csv(cursor)


'''
connection to server details
'''

ctx = mysql.connector.connect(user=NAME, password=NAME, host=HOST, database=NAME)
cursor = ctx.cursor()

main(cursor)

cursor.close()
ctx.close()


'''
API retrieve
'''

result = requests.get('https://api.themoviedb.org/3/movie/550?api_key=7e759b2920f15726a47aecff3b17d4fb')
result_dict = result.json()
print(result_dict['id'])
