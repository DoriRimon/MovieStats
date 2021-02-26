import sys
import os, json
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

sys.path.insert(1, './SRC/')

from globe import *
from flask import Flask, jsonify, request, redirect, render_template
from database import Database


app = Flask(__name__)
db = None


@app.route('/')
def upload_form():
    #Render homepage
    return render_template('index.html')

@app.route('/allGenres')
def fetch_genres():
    # get genres and amount of movies for them
    records = db.search_genre_movies_count()

    # build response
    resp = jsonify(records)
    resp.status_code = 200
    resp.headers.add('Access-Control-Allow-Origin', '*')

    return resp


@app.route('/blocks/<type>/<text>', methods=['GET'])
def render_blocks(type, text):
    # Fetch from db all the names and images found from the full text query
    # type decides whether we query Actor or Movie table
    # render the blocks page accordignly
    
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
    # Fetch top 10 movies and top 10 actors from the db, and their details.
    # render the top 10 of genre page accordignly

    genres = db.search_genre(text)
    if (len(genres) != 1):
        return

    genre = genres[0]

    # full text search
    movies = db.search_genre_movies(genre)
    actors = db.search_genre_actors(genre)

    return render_template('genre.html', movies=movies, actors=actors)


@app.route('/movie/<id>', methods=['GET'])
def render_movie(id):
    #fetch from db movie details of the given id and render movie page,
    #also fetch all the actors of the movie, and 5 recommended movies

    movie = db.search_movie(id)
    actors = db.get_movie_actors(id)
    pos = db.get_movie_position(id)
    rec = db.get_movie_recommendations(id)

    return render_template('movie.html', movie=movie, pos=pos, actors=actors, rec=rec)


@app.route('/actor/<id>', methods=['GET'])
def render_actor(id):
    #fetch from db actpr details of the given id and render actor page
    #also fetch all movies the actor acted in and 5 recommended actors

    actor = db.search_actor(id)
    movies = db.get_actor_movies(id)
    rec = db.get_actor_recommendations(id)

    return render_template('actor.html', actor=actor, movies=movies, rec=rec)


@app.route('/search', methods=['POST'])
def search():
    # run a full text query on the db and return the results
    # table - relevant table from the user select options (Movie / Actor / Genere)
    table = request.form['table']

    # text - user input text
    text = request.form['text']

    
    # full text search
    records = db.ft_search(table, text)

    # build response
    resp = jsonify(records)
    resp.status_code = 200
    resp.headers.add('Access-Control-Allow-Origin', '*')

    return resp

if __name__ == "__main__":
    db = Database()
    db.connect()
    app.run(host=HOST, port=str(PORT), debug=True)
    print('server running at port ', PORT)