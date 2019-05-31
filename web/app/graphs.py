from sqlalchemy.sql import select
import pandas
import plotly
import plotly.plotly as py
import plotly.graph_objs as go
import json
from datetime import datetime,timedelta
from dateutil import tz
from wsutil.models import Observation,Asos_Jfk,Asos_Jrb,Asos_Lga,Asos_Nyc

asrc_keys = ['temp_f','pressure_mb', 'rain_day_in', 'rain_rate_in_per_hr',
             'relative_humidity', 'wind_kt']

asos_keys = ['local_valid']


def fix_utc(t):
    '''Bandaid fix for fixing timezone issue with Observation'''
    return t + timedelta(hours=-4)

def get_now():
    '''current time in local EST'''
    tzlocal = tz.tzoffset('EST', -14400)
    utcnow = datetime.utcnow().replace(tzinfo=tz.tzutc())
    return utcnow.astimezone(tzlocal)

def get_asrc_df(session):
    d = timedelta(days=-7)
    end = get_now()
    start = end + d

    columns = [Observation.datetime, Observation.temp_f,
               Observation.relative_humidity, Observation.pressure_mb, Observation.wind_kt]

    s = select(columns).where(Observation.datetime >= start).where(
        Observation.datetime <= end)
    df = pandas.read_sql(s, session.connection(),
                         parse_dates='datetime')

    #TEMPORARY FIX FOR TIMEZONE ISSUES WITH POSTGRESQL
    #NOTE: Should revise schema to better reflect timezone at some point
    df.datetime = df.datetime.apply(fix_utc)

    return df

def get_asos_df(session):
    dfs = {}
    for model in [Asos_Jfk,Asos_Jrb,Asos_Lga,Asos_Nyc]:
        d = timedelta(days=-7)
        end = get_now()
        start = end + d

        columns = [getattr(model,'local_valid'),getattr(model,'tmpf'),getattr(model,'relh'),getattr(model,'sknt'),getattr(model,'mslp')]
        s = select(columns).where(model.local_valid >= start).where(
        model.local_valid <= end).order_by(model.local_valid)
        df = pandas.read_sql(s, session.connection(),
                         parse_dates='local_valid')
        dfs[model.__station__] = df
    return dfs

def plot_temp(asrc_df,asos_dfs):
    data = [
        go.Scattergl(
            x=asrc_df['datetime'],
            y=asrc_df['temp_f'],
            name='ASRC',
            hoverinfo='y'
        )
    ]

    for station,df in asos_dfs.items():
        data.append(
            go.Scattergl(
            x=df['local_valid'],
            y=df['tmpf'],
            name=station.upper(),
            hoverinfo='y'
        )
        )


    layout = go.Layout(
        title='Temperature',
        yaxis=dict(title='Fahrenheit'),
    )

    fig = go.Figure(data=data, layout=layout)

    return json.dumps(fig, cls=plotly.utils.PlotlyJSONEncoder)

def plot_humidity(asrc_df,asos_dfs):
    data = [
        go.Scattergl(
            x=asrc_df['datetime'],
            y=asrc_df['relative_humidity'],
            name='ASRC',
            hoverinfo='y'
        )
    ]

    for station,df in asos_dfs.items():
        data.append(
            go.Scattergl(
            x=df['local_valid'],
            y=df['relh'],
            name=station.upper(),
            hoverinfo='y'
        )
        )


    layout = go.Layout(
        title='Relative Humidity',
        yaxis=dict(title='Percentage'),
    )

    fig = go.Figure(data=data, layout=layout)

    return json.dumps(fig, cls=plotly.utils.PlotlyJSONEncoder)

def plot_wind(asrc_df,asos_dfs):
    data = [
        go.Scattergl(
            x=asrc_df['datetime'],
            y=asrc_df['wind_kt'],
            name='ASRC',
            hoverinfo='y'
        )
    ]

    for station,df in asos_dfs.items():
        data.append(
            go.Scattergl(
            x=df['local_valid'],
            y=df['sknt'],
            name=station.upper(),
            hoverinfo='y'
        )
        )

    layout = go.Layout(
        title='Wind Speed',
        yaxis=dict(title='Knots'),
    )

    fig = go.Figure(data=data, layout=layout)

    return json.dumps(fig, cls=plotly.utils.PlotlyJSONEncoder)

def plot_pressure(asrc_df,asos_dfs):
    data = [
        go.Scattergl(
            x=asrc_df['datetime'],
            y=asrc_df['pressure_mb'],
            name='ASRC',
            hoverinfo='y'
        )
    ]

    for station,df in asos_dfs.items():
        data.append(
            go.Scattergl(
            x=df['local_valid'],
            y=df['mslp'],
            name=station.upper(),
            hoverinfo='y'
        )
        )

    layout = go.Layout(
        title='Pressure',
        yaxis=dict(title='millibar'),
    )

    fig = go.Figure(data=data, layout=layout)

    return json.dumps(fig, cls=plotly.utils.PlotlyJSONEncoder)

