# views.py

from flask import render_template

from app import app, db

from app.queries import *

from collections import OrderedDict

from datetime import datetime

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
    nyc = nyc_current(db.session)
    asrc_today_avg = asrc_averages(db.session,'day')
    asrc_month_avg = asrc_averages(db.session,'month')
    asrc_recent = asrc_recent_observation(db.session)
    return render_template("index.html",nyc_current=nyc,asrc_today_avg = asrc_today_avg,asrc_month_avg = asrc_month_avg,asrc_recent=asrc_recent)

@app.route('/Records')
def Records():
    return render_template("Records.html")

@app.route('/Charts')
def Charts():
    return render_template("Charts.html")

@app.route('/about')
def about():
    return render_template("about.html")


@app.route('/instruments')
def instruments():
    return render_template("instruments.html")


@app.route('/test')
def test():
    asrc_all_time = asrc_alltime(db.session,keys=SCALARS)

    asrc_now = asrc_current(db.session)

    asos_now = asos_current(db.session,['jfk','lga','jrb','nyc'])

    #nyc = nyc_current(db.session)

    # asos_within_drange = asos_drange(['lga','jfk','jrb','nyc'],datetime(2019,4,25,0),datetime(2019,4,25,23,59))

    # asos_now = asos_current(['jfk','lga','jrb','nyc'])

    return render_template("test.html", asrc_all_time=asrc_all_time, asrc_current=asrc_now)
