from sqlalchemy import MetaData,Table
from sqlalchemy.ext.automap import automap_base
from app import db

db.Model.metadata.reflect(db.engine)

class Observation(db.Model):
    __table__ = db.Model.metadata.tables['observation']

    def __repr__(self):
        pass