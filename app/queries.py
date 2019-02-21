from app.models import Observation


def get_current(session):
    """Return Dictionary of values from most recent observation"""
    pass


def get_alltime(session,key,ascending=False):

    #TODO: Allow for individual key search or return all records of numeric data only
    q = session.query(Observation).order_by(key).all()
    if(ascending):
        return(getattr(q[0],key))
    else:
        return(getattr(q[-1],key))

def get_record(session,datetime):
    row = session.query(Observation).filter_by(datetime=datetime).first()
    return(dict_from_row(row))

def dict_from_row(row):
    keys = row.__table__.columns.keys()
    
    record = {}
    for key in keys:
        record[key] = getattr(row,key)

    return record