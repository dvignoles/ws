# views.py

from flask import render_template

from app import app, db

from app.queries import *
from app.graphs import *

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

@app.route('/records')
def records():
    start_this_year= datetime(datetime.today().year,1,1)
    end_this_year= datetime(datetime.today().year,12,31)

    year_records = asrc_records(asrc_date_range(db.session,start_this_year,end_this_year))
    alltime_records = asrc_records(asrc_all(db.session))

    today = datetime.today()

    return render_template("records.html",today=today,year_records=year_records,alltime_records=alltime_records)

@app.route('/charts')
def charts():
    asrc_df = get_asrc_df(db.session)
    asos_dfs = get_asos_df(db.session)

    temp_plot = plot_temp(asrc_df,asos_dfs)
    humidity_plot = plot_humidity(asrc_df,asos_dfs)
    wind_plot = plot_wind(asrc_df,asos_dfs)
    pressure_plot = plot_pressure(asrc_df,asos_dfs)
    return render_template("charts.html",temp_plot=temp_plot,humidity_plot=humidity_plot,wind_plot=wind_plot,pressure_plot=pressure_plot)

@app.route('/about')
def about():
    return render_template("about.html")


@app.route('/instruments')
def instruments():
    return render_template("instruments.html")