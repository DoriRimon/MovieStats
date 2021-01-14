import os, json
from flask import Flask, jsonify, request, redirect, render_template
import sys
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from Database import Database
from globe import *

app = Flask(__name__)
db = None

@app.route('/')
def upload_form():
    return render_template('index.html')

@app.route('/search', methods=['POST'])
def search():
    # table - relevant table from the user select options (Movie / Actor / Genere)
    table = request.form['table']
    print('table: ', table)

    # text - user input text
    text = request.form['text']
    print('text: ', text)
    
    # full text search
    arr = db.ft_search(table, text)

    # build response
    resp = jsonify(arr)
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