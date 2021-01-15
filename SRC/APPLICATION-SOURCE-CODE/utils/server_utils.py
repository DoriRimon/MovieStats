import sys
import os, json
sys.path.insert(1, './SRC/')

from flask import Flask, jsonify, request, redirect, render_template
from globe import *

def render_page(table, arr):
    if table == 'Movie':
        render_template('movie.html')
        pass
    if table == 'Actor':
        pass
    if table == 'Genre':
        pass
    pass