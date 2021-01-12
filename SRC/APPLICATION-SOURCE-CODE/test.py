import os, json
from flask import Flask, jsonify, request, redirect, render_template
import sys
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from Database import Database
from globe import *

app = Flask(__name__)

db = Database()
db.connect()

@app.route('/')
def upload_form():
	return render_template('index.html')

@app.route('/search', methods=['POST'])
def search():
    term = request.form['q']
    print('term: ', term)
    
    arr = db.search_movie(term)
    filt = [v[0] for v in arr]

    resp = jsonify(filt)
    print(resp)
    resp.status_code = 200
    resp.headers.add('Access-Control-Allow-Origin', '*')
    return resp

if __name__ == "__main__":
    app.run(host=HOST, port=str(PORT), debug=True)
    print('server running at port ', PORT)