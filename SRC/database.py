import sys
import os, json

from globe import *
import pandas as pd
import requests
import mysql.connector
import numpy as np


# The Database class handles all the transactions with the db

class Database:
    def __init__(self):
        self.curser = None
        self.ctx = None

    def connect(self):
        print("connecting to mysql")
        self.ctx = mysql.connector.connect(user=NAME, password=NAME, host=HOST, database=NAME)
        self.cursor = self.ctx.cursor(buffered=True)

    def disconnect(self):
        self.cursor.close()
        self.ctx.close()

    def execute_query(self, query, params=(), commit=False):
        self.cursor.execute(query, params)

        if commit:
            self.ctx.commit()
            return

        res = self.cursor.fetchall()

        return res

    def create_movie_table(self):
        query = ''' create table if not exists Movie (
                    id char(9) not null,
                    title varchar(200) not null,
                    budget int,
                    revenue bigint,
                    releaseDate date,
                    posterPath varchar(100),
                    overview text,
                    rating float(2),
                    primary key (id),
                    fulltext idx (title)
                    ) engine=InnoDB; '''
        self.execute_query(query, commit=True)

    def create_actor_table(self):
        query = ''' create table if not exists Actor (
                    id char(9) primary key,
                    name varchar(100) not null,
                    profilePath varchar(100),
                    biography text,
                    fulltext idx (name)
                    ) engine=InnoDB; '''
        self.execute_query(query, commit=True)

    def create_genre_table(self):
        query = ''' create table if not exists Genre (
                    id int primary key,
                    name varchar(100) not null
                    ); '''
        self.execute_query(query, commit=True)

    def create_movieActor_table(self):
        query = ''' create table if not exists MovieActor (
                    movieID char(9) not null,
                    actorID char(9) not null,
                    foreign key (movieID) references Movie(id),
                    foreign key (actorID) references Actor(id)
                    ); '''
        self.execute_query(query, commit=True)

    def create_movieGenre_table(self):
        query = ''' create table if not exists MovieGenre (
                    movieID char(9) not null,
                    genreID int not null,
                    foreign key (movieID) references Movie(id),
                    foreign key (genreID) references Genre(id)
                    ); '''
        self.execute_query(query, commit=True)

    def drop_table(self, table):
        query = ''' drop table if exists {}; '''.format(table)
        self.execute_query(query, commit=True)

    def insert_movie(self, tuple):
        s = ['%s' for t in tuple]
        r = ', '.join(s)
        query = ''' insert into Movie (id, title, budget, revenue, releaseDate, posterPath, overview, rating)
                    values({}); '''.format(r)
        self.execute_query(query, tuple, commit=True)

    def insert_actor(self, tuple):
        s = ['%s' for t in tuple]
        r = ', '.join(s)
        query = ''' insert into Actor (id, name, profilePath, biography)
                    values({}); '''.format(r)
        self.execute_query(query, tuple, commit=True)

    def insert_genre(self, tuple):
        s = ['%s' for t in tuple]
        r = ', '.join(s)
        query = ''' insert into Genre (id, name)
                    values({}); '''.format(r)
        self.execute_query(query, tuple, commit=True)

    def insert_movie_actor(self, tuple):
        s = ['%s' for t in tuple]
        r = ', '.join(s)
        query = ''' insert into MovieActor (movieID, actorID)
                    values({}); '''.format(r)
        self.execute_query(query, tuple, commit=True)

    def insert_movie_genre(self, tuple):
        s = ['%s' for t in tuple]
        r = ', '.join(s)
        query = ''' insert into MovieGenre (movieID, genreID)
                    values({}); '''.format(r)
        self.execute_query(query, tuple, commit=True)

    def search_genre(self, text):
        query = ''' select  name
                    from    Genre
                    where   name like '%{}%'; '''.format(text)

        print(query)
        
        genres = self.execute_query(query)
        return [v[0] for v in genres]

    def search_movie(self, id):
        query = ''' select  *
                    from    Movie
                    where   id = '{}';
                '''.format(id)

        movie = list(self.execute_query(query)[0])

        movie[6] = movie[6].replace('"', '')
        movie[6] = movie[6].replace('\n', '')

        return movie

    def search_actor(self, id):
        query = ''' select  *
                    from    Actor
                    where   id = '{}';
                '''.format(id)

        actor = list(self.execute_query(query)[0])

        actor[3] = actor[3].replace('"', '')
        actor[3] = actor[3].replace('\n', '')

        return actor


    # full text search
    def ft_search(self, table, text):
        titles = {'Movie' : 'title', 'Actor' : 'name'}
        if table == 'Movie' or table == 'Actor':
            if not text:
                return []
        
            t = self.__format_ft_match_expr(text)

            query = ''' select  {}
                        from    {}
                        where   match({}) against('{}' in boolean mode); '''.format(titles[table], table, titles[table], t)

            print(query)
            
            res = self.execute_query(query)
            return [v[0] for v in res]
        
        if table == 'Genre':
            return self.search_genre(text)
        
        return []


    def ft_list_search(self, table, text, attributes):
        att = ', '.join(attributes)
        titles = {'Movie' : 'title', 'Actor' : 'name'}
        if table == 'Movie' or table == 'Actor':
            if not text:
                return []
        
            t = self.__format_ft_match_expr(text)

            query = ''' select  {}, id
                        from    {}
                        where   match({}) against('{}' in boolean mode); '''.format(att, table, titles[table], t)

            print(query)
            
            res = self.execute_query(query)
            return [list(v) for v in res]
        
        return []

    
    def search_genre_movies(self, genre):
        query = ''' select      Movie.title, Movie.posterPath, (Movie.revenue - Movie.budget) as pureRevenue,
                                Movie.overview, Movie.id
                    from        Movie, MovieGenre, Genre
                    where       Movie.id = MovieGenre.movieID and
                                Genre.id = MovieGenre.genreID 
                                and Genre.name = '{}'
                                and Movie.revenue > 0
                                and Movie.budget > 0
                    order by    pureRevenue desc
                    limit       10;
                '''.format(genre)

        movies = self.execute_query(query)
        movies =  [list(v) for v in movies]

        for movie in movies:
            movie[3] = movie[3].replace('"', '')
            movie[3] = movie[3].replace('\n', '')

        return movies

    def search_genre_actors(self, genre):
        query = ''' select      Actor.name, Actor.profilePath, Actor.biography, count(*) AS amount, Actor.id
                    from        Actor, Movie, MovieActor, MovieGenre, Genre
                    where       Actor.id = MovieActor.actorID and
                                Movie.id = MovieActor.movieID and
                                MovieGenre.genreID = Genre.id and
                                MovieGenre.movieID = Movie.id and Genre.name = '{}'
                    group by    Actor.id
                    order by    amount desc
                    limit       10;       
                '''.format(genre)

        actors = self.execute_query(query)
        actors = [list(v) for v in actors]

        for actor in actors:
            actor[2] = actor[2].replace('"', '')
            actor[2] = actor[2].replace('\n', '')

        return actors
    
    def search_genre_movies_count(self):
        query = ''' select 		Genre.name, count(*) as totalMovies
                    from		Movie, MovieGenre, Genre
                    where		Movie.id = MovieGenre.movieID and
                                MovieGenre.genreID = Genre.id
                    group by	Genre.id
                    order by	totalMovies desc;
                '''
        
        genres = self.execute_query(query)
        genres = [list(v) for v in genres]

        return genres


    def get_movie_actors(self, id):
        query = ''' select      Actor.name, Actor.profilePath, Actor.id
                    from        Actor, Movie, MovieActor
                    where       Actor.id = MovieActor.actorID and
                                Movie.id = MovieActor.movieID and Movie.id = '{}';
                '''.format(id)
        
        actors = self.execute_query(query)
        return [list(v) for v in actors]

    
    def get_movie_position(self, id):
        query = ''' select  (count(*) + 1) as globalRating
                    from    Movie
                    where   Movie.rating > (    select Movie.rating
                                                from Movie
                                                where Movie.id = '{}' );
		
                '''.format(id)
        
        rating = self.execute_query(query)
        return rating[0][0]

    
    def get_movie_recommendations(self, id):
        query = ''' select      M1.id, M1.title, M1.posterPath
                    from        Movie as M1, Actor, MovieActor
                    where       M1.id = MovieActor.movieID and 
                                Actor.id = MovieActor.actorID and
                                Actor.id IN (   select A2.id
                                                from Movie as M2, Actor as A2, MovieActor as MA2
                                                where M2.id = MA2.movieID and 
                                                A2.id = MA2.actorID and M2.id = '{}' and
                                                M1.id <> M2.id  )
                    group by    M1.id
                    order by    count(*) desc
                    limit       5;
                '''.format(id)

        rec = self.execute_query(query)
        return [list(v) for v in rec]

    
    def get_actor_movies(self, id):
        query = ''' select  Movie.title, Movie.posterPath, Movie.id
                    from    Movie, MovieActor, Actor
                    where   Actor.id = MovieActor.actorID and
                            Movie.id = MovieActor.movieID and Actor.id = '{}'
                '''.format(id)

        movies = self.execute_query(query)
        return [list(v) for v in movies]


    def get_actor_recommendations(self, id):
        query = ''' select      A1.name, A1.profilePath, A1.id
                    from        Movie, Actor as A1, MovieActor
                    where       Movie.id = MovieActor.movieID and 
                                A1.id = MovieActor.actorID and
                                Movie.id IN (   select M2.id
                                                from Movie as M2, Actor as A2, MovieActor as MA2
                                                where M2.id = MA2.movieID and 
                                                        A2.id = MA2.actorID and A2.id = '{}' and
                                                        A1.id <> A2.id  )
                    group by A1.id
                    order by count(*) desc
                    limit 5;
                '''.format(id)

        rec = self.execute_query(query)
        return [list(v) for v in rec]


    def __rep(self, s):
	    return s.replace('-', ' ') 

    def __format_ft_match_expr(self, text):
        words = text.split()
        words = list(map(self.__rep, words))
        bf = ['+' + word if len(word) > 3 or index == (len(words) - 1) else word for index, word in enumerate(words)] # creating boolean format
        bf[-1] += '*'
        t = ' '.join(bf)
        return t