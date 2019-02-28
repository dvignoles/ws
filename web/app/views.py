# views.py

from flask import render_template

from app import app,db

from app.queries import get_alltime,get_record

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
    wind_mph = get_alltime(db.session,'wind_mph')
    return render_template("test.html",wind_mph=wind_mph)