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

        res = self.cursor.fetchall()

        return res

    def create_movie_table(self):
        query = ''' create table if not exists movie (
                    id char(9) not null,
                    title varchar(200) not null,
                    primary key (id),
                    fulltext idx (title)
                    ) engine=InnoDB; '''
        self.execute_query(query, commit=True)

    def drop_movie_table(self):
        query = ''' drop table movie; '''
        self.execute_query(query, commit=True)

    def insert_movie(self, tuple):
        query = ''' insert into movie (id, title)
                    values(%s, %s); '''
        self.execute_query(query, tuple, commit=True)

    def search_movie(self, text):
        if not text:
            return []
        
        words = text.split()
        bf = ['+' + word if len(word) > 2 else word for word in words] # creating boolean format
        bf[-1] += '*'
        t = ' '.join(bf)

        query = ''' select  title
                    from    movie
                    where   match(title) against('{}' in boolean mode); '''.format(t)

        print(query)
        
        movies = self.execute_query(query)
        return [v[0] for v in movies]

    def ft_search(self, table, text):
        if table == 'movie':
            return self.search_movie(text)
        

    
