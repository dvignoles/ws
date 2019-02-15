# views.py

from flask import render_template

from app import app

@app.route('/')
def index():
    return render_template("HomePage.html")


@app.route('/about')
def about():
    return render_template("about.html")

@app.route('/instruments')
def instruments():
	return render_template("Instruments.html")

@app.route('/test')
def test():
	return render_template("test.html")