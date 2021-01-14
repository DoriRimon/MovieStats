import os
import numpy as np
import pandas as pd
import requests
import json
import mysql.connector
from Database import Database
import zipfile
from globe import *


# extract csv files
with zipfile.ZipFile(PATH_PREFIX + '/APPLICATION-SOURCE-CODE/static/data/data.zip', 'r') as zip_ref:
    zip_ref.extractall(PATH_PREFIX + '/APPLICATION-SOURCE-CODE/static/data')


# return    : df
# shape     : id, rating
# content   : globe.MOVIES_BATCH_SIZE heighest rated movies
def filter_movies_csv():
    df = pd.read_csv(PATH_PREFIX + "/APPLICATION-SOURCE-CODE/static/data/ratings.csv", usecols=['imdb_title_id', 'weighted_average_vote'])
    df.rename(columns={'imdb_title_id': 'movie_id', 'weighted_average_vote': 'rating'}, inplace=True)
    df['movie_id'] = df['movie_id'].astype('str')
    exp = (df['movie_id'].str.len() == 9)
    df = df.loc[exp]
    res = df.nlargest(MOVIES_BATCH_SIZE, 'rating')
    print(res.head())
    print(res.tail())
    return res


# return    : df
# shape     : actor_id
# content   : relevant (play in existing movies) actors ids
def filter_actors_csv(movieActors_df):
    movieActors_df = movieActors_df.drop(['movie_id'], axis=1)
    res =  movieActors_df.drop_duplicates('actor_id')
    print(res.head())
    print(res.tail())
    return res


# return    : df
# shape     : movie_id, actor_id
# content   : connects between movie ids and relevant (play in existing movies) actors ids
def filter_movieActors_csv(movies_df):
    df = pd.read_csv(PATH_PREFIX + "/APPLICATION-SOURCE-CODE/static/data/movie_actors.csv", usecols=['imdb_title_id', 'imdb_name_id', 'category'])
    df.rename(columns={'imdb_title_id': 'movie_id', 'imdb_name_id': 'actor_id'}, inplace=True)
    df = df.merge(movies_df, how='inner', on='movie_id')
    df['category'] = df['category'].astype('str')
    df = df.loc[(df['category'] == 'actress') | (df['category'] == 'actor')]
    df['actor_id'] = df['actor_id'].astype('str')
    df = df.loc[(df['actor_id'].str.len() == 9)]
    df = df.drop(['category', 'rating'], axis=1)
    print(df.head())
    print(df.tail())
    return df


if RUN_LOCALLY:
    movies_df = filter_movies_csv()
    movieActors_df = filter_movieActors_csv(movies_df)
    actors_df = filter_actors_csv(movieActors_df)
