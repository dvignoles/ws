from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy import Column, String, Integer, Float, DateTime, Date, Time
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.exc import IntegrityError
from WeatherLinkScrape import get_soup,send_email
from datetime import datetime as dt
from time import sleep
import os

Base = declarative_base()
class Observation(Base):
    __tablename__ = 'observation'

    datetime = Column('datetime',DateTime(),unique=True,primary_key=True)
    station_name = Column('station_name', String(255),unique=False)
    location = Column('location', String(255), unique=False)
    latitude = Column('latitude', Float(), unique=False)
    longitude = Column('longitude', Float(), unique=False)
    date = Column('date',Date(),unique=False)
    time = Column('time',Time(),unique=False)
    timezone = Column('timezone',String(255),unique=False)
    dewpoint_c = Column('dewpoint_c', Float(), unique=False)
    dewpoint_f = Column('dewpoint_f', Float(), unique=False)
    heat_index_c = Column('heat_index_c', Float(), unique=False)
    heat_index_f = Column('heat_index_f', Float(), unique=False)
    pressure_in = Column('pressure_in', Float(), unique=False)
    pressure_mb = Column('pressure_mb', Float(), unique=False)
    relative_humidity = Column('relative_humidity', Integer(),unique=False)
    solar_radiation = Column('solar_radiation', Integer(), unique=False)
    sunrise = Column('sunrise', String(255), unique=False)
    sunset = Column('sunset', String(255), unique=False)
    temp_c = Column('temp_c', Float(), unique=False)
    temp_f = Column('temp_f', Float(), unique=False)
    uv_index = Column('uv_index', Float(), unique=False)
    wind_degrees = Column('wind_degrees', Integer(), unique=False)
    wind_dir = Column('wind_dir', String(255), unique=False)
    wind_kt = Column('wind_kt', Float(), unique=False)
    wind_mph = Column('wind_mph', Float(), unique=False)
    windchill_c = Column('windchill_c', Float(), unique=False)
    windchill_f = Column('windchill_f', Float(), unique=False)

def db_init(DB_URI):
    engine = create_engine(DB_URI)
    Base.metadata.create_all(engine)
    Session = sessionmaker(bind=engine)
    return(Session)

def db_record(url,Session):
    """
        Record from xml url to database connection on ten minute interval
    """
    error_count = 0
    while True:
        session = Session()
        observation = Observation(**get_soup(url))
        try:
            session.add(observation)
            session.commit()
            print('Observation successfully recorded to database at: ',str(dt.now()))
            error_count = 0
        except IntegrityError:
            print('No new Observation Found at: ',str(dt.now()))
            error_count += 1
        except:
            print('Unnacounted for Error')
        finally:
            session.close()
            if error_count == 0:
                sleep(600) #10 min
            elif error_count < 11:
                sleep(60) #1 min * 10
            elif error_count < 16:
                sleep(600) #10 min * 5
            else:
                print('Alert Triggered') 
                # if os.environ.get('') is not None:
                #     message = """\
                #     Subject: Alert

                #     Weather Station is stalled. 
                #     """
                #     send_email(alert['sender'],alert['sender_pass'],alert['receiver'],message)
                sleep(3600 * 6) #1 hour * 6

