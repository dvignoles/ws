'''
    Utility functions for sqlalchemy tasks
'''

from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from models import Base

def db_init(DB_URI):
    """
        Connect to database and return Session object
    """
    engine = create_engine(DB_URI)
    Base.metadata.create_all(engine)
    Session = sessionmaker(bind=engine)
    return(Session)