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
        self.cursor = self.ctx.cursor()

    def disconnect(self):
        self.cursor.close()
        self.ctx.close()

    def execute_query(self, query, params):
        res = cursor.execute(query, params)
        ctx.commit()
        return res

    def create_movie_table(self):
        # genre varchar(100),
        # duration int, 
        # lang varchar(100), 
        # budget int, 
        # income int, 
        # year int,
        query = ''' create table if not exists movie (
                    id char(9) not null,
                    title varchar(200) not null
                    primary key (id)
                    fulltext idx (title)) engine = InnoDB'''

    def insert_movie(self, tuple):
        query = ''' insert into movie (
                        values(%s, %s)
                    )
                '''
        self.execute_query(query, tuple)

    def search_movie(self, text):
        query = ''' select  title
                    from    movie
                    where   match(title) against(%s in natural language mode)
                '''
        movies = self.query(query, [text])
        return movies

    