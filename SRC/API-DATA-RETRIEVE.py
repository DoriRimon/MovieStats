import os.path
import numpy as np
import pandas as pd
import requests
import json
import mysql.connector
from globe import *
from Database import Database
from data_fill import *
from datetime import datetime


# create Database object
db = Database()


# insert genres from api to db
def genres_from_api_to_db():
    genres = requests.get(BASE_API_URL + '/genre/movie/list?api_key={}'.format(API_KEY))
    genresArr = genres.json()['genres']
    for genre in genresArr:
        db.insert_genre((genre['id'], genre['name']))
    print("Genres are alive")


# insert movies from api to db
def movies_from_api_to_db(movies_df):
    for index, row in movies_df.iterrows():
        findMovieRes = requests.get(BASE_API_URL + "/find/{}?api_key={}&external_source=imdb_id".format(row['id'], API_KEY))
        if findMovieRes.status_code == 200:
            foundMovie = findMovieRes.json()
            if not foundMovie['movie_results']:
                continue
            id = str(foundMovie['movie_results'][0]['id'])
            movieDetailsRes = requests.get(BASE_API_URL + "/movie/{}?api_key={}&language=en-US".format(id, API_KEY))
            if movieDetailsRes.status_code == 200:
                movieDetails = movieDetailsRes.json()
                db.insert_movie((row['id'], movieDetails['original_title'], movieDetails['budget'], movieDetails['revenue'], \
                (datetime.strptime(movieDetails['release_date'], '%Y-%m-%d') if movieDetails['release_date'] else None), \
                movieDetails['poster_path'], movieDetails['overview'], row['rating']))
                for genre in movieDetails['genres']:
                    db.insert_movie_genre((row['id'], genre['id']))
        if index % 1000 == 0:
            print('inserted {} movies'.format(index))
    print("Movies are alive")


# insert actors from api to db
def actors_from_api_to_db(actors_df):
    for index, row in actors_df.iterrows():
        findActorRes = requests.get(BASE_API_URL + "/find/{}?api_key={}&external_source=imdb_id".format(row['actor_id'], API_KEY))
        if findActorRes.status_code == 200:
            foundActor = findActorRes.json()
            if not foundActor['person_results']:
                continue
            id = str(foundActor['person_results'][0]['id'])
            actorDetailsRes = requests.get(BASE_API_URL + "/person/{}?api_key={}&language=en-US".format(id, API_KEY))
            if actorDetailsRes.status_code == 200:
                actorDetails = actorDetailsRes.json()
                db.insert_actor((row['actor_id'], actorDetails['name'], actorDetails['profile_path'], actorDetails['biography']))
        if index % 1000 == 0:
            print('inserted {} actors'.format(index))
    print("Actors are alive")


# insert actorMovies from csv to db
def actor_movie_from_csv_to_db(movieActors_df):
    for _, row in movieActors_df.iterrows():
        try:
            db.insert_movie_actor((row['movie_id'], row['actor_id']))
        except mysql.connector.IntegrityError as err: # skip foreign key constraint fails
            print(err)
            continue


def main():
    # connect to db
    db.connect()

    ''' 
    # drop existing tables
    drop = ['MovieGenre', 'MovieActor', 'Movie', 'Actor', 'Genre']
    for table in drop:
        db.drop_table(table)

    # create all tables
    db.create_genre_table()
    db.create_actor_table()
    db.create_movie_table()
    db.create_movieActor_table()
    db.create_movieGenre_table()
    '''

    # filter csv data
    movies_df = filter_movies_csv()
    movieActors_df = filter_movieActors_csv(movies_df)
    actors_df = filter_actors_csv(movieActors_df)

    # fill tables
    '''
    genres_from_api_to_db()
    movies_from_api_to_db(movies_df)
    actors_from_api_to_db(actors_df)
    '''
    actor_movie_from_csv_to_db(movieActors_df)

    # disconnect from db
    db.disconnect()


if __name__ == '__main__':
    main()