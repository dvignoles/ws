from wsutil.models import Observation,Asos_Jfk,Asos_Jrb,Asos_Lga,Asos_Nyc
from sqlalchemy import desc
from collections import OrderedDict
from app import db


ASRC_DATA_VAR = ['datetime', 'sunrise', 'sunset','temp_f', 'dewpoint_f','heat_index_f', 
   'pressure_mb', 'rain_day_in', 'relative_humidity', 'solar_radiation', 'uv_index',
   'wind_degrees', 'wind_dir', 'wind_kt', 'windchill_f']

#coversion for analagous asrc/asos variables
asrc_asos = {'datetime':'local_valid','temp_f':'tmpf','dewpoint_f':'dwpf',
'pressure_mb':'mslp','relative_humidity':'relh','rain_day_in':'pday','wind_kt':'sknt','wind_degrees':'drct'}

def dict_from_row(row,keep_keys=None):
    keys = row.__table__.columns.keys()

    if keep_keys:
        assert(set(keep_keys).issubset(keys))
        keys = keep_keys

    record = {}
    for key in keys:
        record[key] = getattr(row, key)

    return record

def asrc_current(keys=None):
    """Return Dictionary of values from most recent observation"""
    q = db.session.query(Observation).order_by(desc(Observation.datetime)).first()
    return dict_from_row(q,keep_keys=keys)


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

def asos_current(stations,keys=None):
    station_observations = {}
    for station in stations:
        table = choose_asos(station)
        station_observations[table.__station__] = dict_from_row(db.session.query(table)[-1],keep_keys=keys)
    return station_observations

def nyc_current():
    asrc_now = asrc_current(keys = asrc_asos.keys())
    asos_now = asos_current(['jfk','lga','jrb','nyc'],keys = asrc_asos.values())

    results = {}
    for asrc,asos in asrc_asos.items():
        key = asrc
        if key == 'datetime':
            key ='update_time'
        results[key] = {'asrc':asrc_now[asrc],'jfk':asos_now['jfk'][asos],'lga':asos_now['lga'][asos],'jrb':asos_now['jrb'][asos],'nyc':asos_now['nyc'][asos]}

    return results
    
