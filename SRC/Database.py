from globe import *
import os.path
import pandas as pd
import requests
import json
import mysql.connector
import numpy as np

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
                    revenue int,
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
        query = ''' IF OBJECT_ID('{}', 'U') IS NOT NULL DROP TABLE {}; '''.format(table, table)
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
        query = ''' insert into movie (id, name)
                    values({}); '''.format(r)
        self.execute_query(query, tuple, commit=True)

    def insert_movie_actor(self, tuple):
        s = ['%s' for t in tuple]
        r = ', '.join(s)
        query = ''' insert into movie (movieID, actorID)
                    values({}); '''.format(r)
        self.execute_query(query, tuple, commit=True)

    def insert_movie_genre(self, tuple):
        s = ['%s' for t in tuple]
        r = ', '.join(s)
        query = ''' insert into movie (movieID, genreID)
                    values({}); '''.format(r)
        self.execute_query(query, tuple, commit=True)

    def serach_genre(self, text):
        query = ''' select  name
                    from    Genre
                    where   name like '%{}%'; '''.format(text)

        print(query)
        
        movies = self.execute_query(query)
        return [v[0] for v in movies]

    def ft_search(self, table, text):
        titles = {'Movie' : 'title', 'Actor' : 'name'}
        if table == 'Movie' or table == 'Actor':
            if not text:
                return []
        
            words = text.split()
            bf = ['+' + word if len(word) > 2 else word for word in words] # creating boolean format
            bf[-1] += '*'
            t = ' '.join(bf)

            query = ''' select  {}
                        from    {}
                        where   match({}) against('{}' in boolean mode); '''.format(titles[table], table, titles[table], t)

            print(query)
            
            movies = self.execute_query(query)
            return [v[0] for v in movies]
        
        if table == 'Genre':
            return self.serach_genre(text)
        
        return []
        

    
