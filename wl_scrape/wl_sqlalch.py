from sqlalchemy import create_engine,MetaData, Table, insert
from sqlalchemy import Column, String, Integer, Float, DateTime, Date, Time
from sqlalchemy.exc import IntegrityError
from WeatherLinkScrape import get_soup,send_email
from datetime import datetime as dt
from time import sleep
import os

metadata = MetaData()

observation = Table('observation',metadata,
    Column('station_name', String(255),unique=False),
    Column('location', String(255), unique=False),
    Column('latitude', Float(), unique=False),
    Column('longitude', Float(), unique=False),
    Column('datetime',DateTime(),unique=True,primary_key=True),
    Column('date',Date(),unique=False),
    Column('time',Time(),unique=False),
    Column('timezone',String(255),unique=False),
    Column('dewpoint_c', Float(), unique=False),
    Column('dewpoint_f', Float(), unique=False),
    Column('heat_index_c', Float(), unique=False),
    Column('heat_index_f', Float(), unique=False),
    Column('pressure_in', Float(), unique=False),
    Column('pressure_mb', Float(), unique=False),
    Column('relative_humidity', Integer(),unique=False),
    Column('solar_radiation', Integer(), unique=False),
    Column('sunrise', String(255), unique=False),
    Column('sunset', String(255), unique=False),
    Column('temp_c', Float(), unique=False),
    Column('temp_f', Float(), unique=False),
    Column('uv_index', Float(), unique=False),
    Column('wind_degrees', Integer(), unique=False),
    Column('wind_dir', String(255), unique=False),
    Column('wind_kt', Float(), unique=False),
    Column('wind_mph', Float(), unique=False),
    Column('windchill_c', Float(), unique=False),
    Column('windchill_f', Float(), unique=False)
)

def db_init(DB_URI):
    engine = create_engine(DB_URI)
    connection = engine.connect()
    metadata.create_all(engine)
    return(connection)

def db_record(url,connection):
    """
        Record from xml url to database connection on ten minute interval
    """
    error_count = 0
    while True:
        soup = get_soup(url)
        query = insert(observation).values(soup)
        try:
            ResultProxy = connection.execute(query)
            print('Observation successfully recorded to database at: ',str(dt.now()))
            error_count = 0
        except IntegrityError:
            print('No new Observation Found at: ',str(dt.now()))
            error_count += 1
        finally:
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

