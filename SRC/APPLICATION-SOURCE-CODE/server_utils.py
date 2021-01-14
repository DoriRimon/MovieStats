from flask import Flask, jsonify, request, redirect, render_template

def render_page(table, arr):
    if table == 'Movie':
        render_template('movie.html')
        pass
    if table == 'Actor':
        pass
    if table == 'Genre':
        pass
    pass