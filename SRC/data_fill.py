import os
import numpy as np
import pandas as pd
import requests
import json
import mysql.connector
from Database import Database
import zipfile

with zipfile.ZipFile('SRC/APPLICATION-SOURCE-CODE/static/data/data.zip', 'r') as zip_ref:
    zip_ref.extractall('SRC/APPLICATION-SOURCE-CODE/static/data')

def filter_movies_csv():
    df = pd.read_csv("SRC/APPLICATION-SOURCE-CODE/static/data/ratings.csv", usecols=['imdb_title_id', 'weighted_average_vote'])
    df.rename(columns={'imdb_title_id': 'id', 'weighted_average_vote': 'rating'}, inplace=True)
    df['id'] = df['id'].astype('str')
    exp = (df['id'].str.len() == 9)
    df = df.loc[exp]
    return df.nlargest(4_000, 'rating')


def filter_actors_csv(movieActors_df):
    movieActors_df = movieActors_df.drop(['movie_id'], axis=1)
    return movieActors_df.drop_duplicates('actor_id')


def filter_movieActors_csv(movies_df):
    df = pd.read_csv("SRC/APPLICATION-SOURCE-CODE/static/data/movie_actors.csv", usecols=['imdb_title_id', 'imdb_name_id', 'category'])
    df.rename(columns={'imdb_title_id': 'movie_id', 'imdb_name_id': 'actor_id'}, inplace=True)
    movies_df.rename(columns={'id' : 'movie_id'}, inplace=True)
    df = df.merge(movies_df, how='inner', on='movie_id')
    df['category'] = df['category'].astype('str')
    df = df.loc[(df['category'] == 'actress') | (df['category'] == 'actor')]
    df = df.drop(['category', 'rating'], axis=1)
    return df


movies_df = filter_movies_csv()
print(len(movies_df.index))
print(movies_df.head())

movieActors = filter_movieActors_csv(movies_df)
print(len(movieActors.index))
print(movieActors.head())

actors_df = filter_actors_csv(movieActors)
print(len(actors_df.index))
print(actors_df.head())