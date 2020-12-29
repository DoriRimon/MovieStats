import os.path
import pandas as pd
import requests
import json
import mysql.connector

NAME = 'DbMysql04'
HOST = 'mysqlsrv1.cs.tau.ac.il'
LOCAL = '127.0.0.1'

# retrieve data form csv

def push_csv(curser):
    df = pd.read_csv('./APPLICATION-SOURCE-CODE/static/data/movies.csv')
    for index, row in df.iterrows():
        query_params = row['imdb_title_id'], row['title']
        query = 'insert into movie_names (id, name) values (%d, %s)'
        curser.execute(query, query_params, multi=False) 

# connection to server details

# my_sql_connector

ctx = mysql.connector.connect(user=NAME, password=NAME, host=HOST, database=NAME)
cursor = ctx.cursor()

query = 'CREATE TABLE IF NOT EXISTS movie_names (id INT PRIMARY KEY, name VARCHAR(100) NOT NULL)'

cursor.execute(query)
push_csv(cursor)

cursor.close()
ctx.close()

# retrieve data from API

result = requests.get('https://api.themoviedb.org/3/movie/550?api_key=7e759b2920f15726a47aecff3b17d4fb')
# check result
result_dict = result.json()
print(result_dict['id'])

# definitions on how to insert different data to DB

# insert data to DB