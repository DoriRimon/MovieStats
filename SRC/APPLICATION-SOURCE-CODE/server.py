import sys
import os, json
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

sys.path.insert(1, './SRC/')

from globe import *
from flask import Flask, jsonify, request, redirect, render_template
from database import Database
from server_utils import render_page


app = Flask(__name__)
db = None


@app.route('/')
def upload_form():
    return render_template('index.html')


@app.route('/blocks/<type>/<text>', methods=['GET'])
def render_blocks(type, text):
    # text - user input text
    print('type: ', type)
    print('text: ', text)
    
    attributes = []
    if type == 'Movie':
        attributes = ['title', 'posterPath']
        
    if type == 'Actor':
        attributes = ['name', 'profilePath']

    # full text search
    records = db.ft_list_search(type, text, attributes)

    return render_template('blocks.html', type=type, records=records)


@app.route('/top/<text>', methods=['GET'])
def render_top(text):
    # text - user input text
    print('text: ', text)

    genres = db.search_genre(text)
    if (len(genres) != 1):
        return

    genre = genres[0]

    # full text search
    movies = db.search_genre_movies(genre)
    actors = db.search_genre_actors(genre)

    for movie in movies:
        movie[3] = movie[3].replace('"', '')
        movie[3] = movie[3].replace('\n', '')

    for actor in actors:
        actor[2] = actor[2].replace('"', '')
        actor[2] = actor[2].replace('\n', '')


    return render_template('genre.html', movies=movies, actors=actors)


@app.route('/search', methods=['POST'])
def search():
    # table - relevant table from the user select options (Movie / Actor / Genere)
    table = request.form['table']
    print('table: ', table)

    # text - user input text
    text = request.form['text']
    print('text: ', text)

    
    # full text search
    records = db.ft_search(table, text)

    # build response
    resp = jsonify(records)
    print(resp)
    resp.status_code = 200
    resp.headers.add('Access-Control-Allow-Origin', '*')

    return resp


if __name__ == "__main__":
    if RUN_LOCALLY:
        app.run()
    else:
        db = Database()
        db.connect()
        app.run(host=HOST, port=str(PORT), debug=True)
        print('server running at port ', PORT)