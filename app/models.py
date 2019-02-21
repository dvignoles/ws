from sqlalchemy import MetaData
from sqlalchemy.ext.automap import automap_base
from app import db

engine = db.engine
metadata = MetaData()
metadata.reflect(engine,only=['observation'])

Base = automap_base(metadata=metadata)

Base.prepare()

Observation = Base.classes.observation