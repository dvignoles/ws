from app import Observation
from sqlalchemy import desc
from collections import OrderedDict

#TODO: Switch from passing in session to Query Objects

def get_current(session):
    """Return Dictionary of values from most recent observation"""
    q = session.query(Observation).order_by(desc(Observation.datetime)).first()
    return(dict_from_row(q))


def get_alltime(session, keys):
    """Return First and Last values for sorted key in keys"""
    all_time = OrderedDict()

    for key in keys:
        q = session.query(Observation).order_by(key).all()

        low = {'val': getattr(q[0], key), 'date': q[0].date.isoformat(
        ), 'time': q[0].time.isoformat()}
        high = {'val': getattr(
            q[-1], key), 'date': q[-1].date.isoformat(), 'time': q[-1].time.isoformat()}

        all_time[key] = {'low': low, 'high': high,
                         'units': get_units(Observation, key)}
    return(all_time)


def get_record(session, datetime):
    #TODO: Query by partial date/time
    row = session.query(Observation).filter_by(datetime=datetime).first()
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


def dict_from_row(row):
    keys = row.__table__.columns.keys()

    record = {}
    for key in keys:
        record[key] = getattr(row, key)

    return record
