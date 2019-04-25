from wsutil.models import Observation,Asos_Jfk,Asos_Jrb,Asos_Lga,Asos_Nyc
from sqlalchemy import desc
from collections import OrderedDict
from app import db

#TODO: Switch from passing in db.session to Query Objects

def dict_from_row(row):
    keys = row.__table__.columns.keys()

    record = {}
    for key in keys:
        record[key] = getattr(row, key)

    return record

def asrc_current():
    """Return Dictionary of values from most recent observation"""
    q = db.session.query(Observation).order_by(desc(Observation.datetime)).first()
    return(dict_from_row(q))


def asrc_alltime(keys):
    """Return First and Last values for sorted key in keys"""
    all_time = OrderedDict()

    for key in keys:
        q = db.session.query(Observation).order_by(key).all()

        low = {'val': getattr(q[0], key), 'date': q[0].date.isoformat(
        ), 'time': q[0].time.isoformat()}
        high = {'val': getattr(
            q[-1], key), 'date': q[-1].date.isoformat(), 'time': q[-1].time.isoformat()}

        all_time[key] = {'low': low, 'high': high,
                         'units': get_units(Observation, key)}
    return(all_time)


def asrc_get_record(datetime):
    #TODO: Query by partial date/time
    row = db.session.query(Observation).filter_by(datetime=datetime).first()
    return(dict_from_row(row))


def get_units(model, column, abbreviated=True):
    """
    If available, return the units string for a given column
    If abbreviated is False, returns the complete unit name
    """
    info = getattr(getattr(model, column), 'info')
    if abbreviated:
        try:
            units_abbrev = info['units_abbrev']
            return units_abbrev
        except:
            return ''
    else:
        try:
            units = info['units']
            return units
        except:
            return ''

def choose_asos(station):
    station = station.lower()
    if station == 'nyc':
        return Asos_Nyc
    elif station == 'jfk':
        return Asos_Jfk
    elif station == 'lga':
        return Asos_Lga
    elif station == 'jrb':
        return Asos_Jrb
    else:
        return None

def asos_drange_avail(station):
    table = choose_asos(station)
    q = db.session.query(table)
    return q[0].local_valid, q[-1].local_valid

def asos_drange(stations,start,end):
    station_observations = {}
    for station in stations:
        table = choose_asos(station)
        station_observations[table.__station__] = db.session.query(table).filter(table.local_valid >= start, table.local_valid <= end)
    
    return station_observations #{'jfk':rows,'lga':rows ... etc}

def asos_current(stations):
    station_observations = {}
    for station in stations:
        table = choose_asos(station)
        station_observations[table.__station__] = db.session.query(table)[-1]
    return station_observations
    
