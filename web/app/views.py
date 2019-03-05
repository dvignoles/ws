# views.py

from flask import render_template

from app import app, db

from app.queries import get_alltime, get_record, get_current

from collections import OrderedDict

# KEYS
META_DATA = ['station_name', 'location', 'latitude', 'longitude', 'timezone']

DATE_TIME = ['datetime', 'date', 'time']

SCALARS = [
    'dewpoint_c', 'dewpoint_f', 'heat_index_c', 'heat_index_f', 'pressure_in', 'pressure_mb', 'relative_humidity', 'solar_radiation',
    'sunrise', 'sunset', 'temp_c', 'temp_f', 'wind_kt', 'wind_mph',
    'windchill_c', 'windchill_f'
]

FACTORS = [
    'wind_degrees', 'wind_dir','uv_index'
]


@app.route('/')
def index():
    return render_template("index.html")


@app.route('/about')
def about():
    return render_template("about.html")


@app.route('/instruments')
def instruments():
    return render_template("instruments.html")


@app.route('/test')
def test():

    all_time = get_alltime(db.session, keys=SCALARS)

    current = get_current(db.session)

    return render_template("test.html", all_time=all_time, current=current)
