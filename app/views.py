# views.py

from flask import render_template

from app import app

@app.route('/')
def index():
    return render_template("HomePage.html")


@app.route('/about')
def about():
    return render_template("about.html")