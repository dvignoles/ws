from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import Column, String, Integer, Float, DateTime, Date, Time


Base = declarative_base()


class Observation(Base):
    __tablename__ = 'observation'

    datetime = Column('datetime', DateTime(), unique=True, primary_key=True)
    station_name = Column('station_name', String(255), unique=False)
    location = Column('location', String(255), unique=False)
    latitude = Column('latitude', Float(), unique=False)
    longitude = Column('longitude', Float(), unique=False)
    date = Column('date', Date(), unique=False)
    time = Column('time', Time(), unique=False)
    timezone = Column('timezone', String(255), unique=False)
    dewpoint_c = Column('dewpoint_c', Float(), unique=False, info={
                        'units': 'Celsius', 'units_abbrev': u'\N{DEGREE SIGN}C'})
    dewpoint_f = Column('dewpoint_f', Float(), unique=False, info={
                        'units': 'Fahrenheit', 'units_abbrev': u'\N{DEGREE SIGN}F'})
    heat_index_c = Column('heat_index_c', Float(), unique=False, info={
                          'units': 'Celsius', 'units_abbrev': u'\N{DEGREE SIGN}C'})
    heat_index_f = Column('heat_index_f', Float(), unique=False, info={
                          'units': 'Fahrenheit', 'units_abbrev': u'\N{DEGREE SIGN}F'})
    pressure_in = Column('pressure_in', Float(), unique=False, info={
                         'units': 'inch of Mercury', 'units_abbrev': 'inHg'})
    pressure_mb = Column('pressure_mb', Float(), unique=False, info={
                         'units': 'millibar', 'units_abbrev': 'mb'})
    relative_humidity = Column('relative_humidity', Integer(), unique=False, info={
                               'units': 'percent', 'units_abbrev': '%'})
    solar_radiation = Column('solar_radiation', Integer(), unique=False, info={
                             'units': 'Watts/meter'+u'\N{SUPERSCRIPT TWO}', 'units_abbrev': 'W/m'+u'\N{SUPERSCRIPT TWO}'})
    sunrise = Column('sunrise', String(255), unique=False)
    sunset = Column('sunset', String(255), unique=False)
    temp_c = Column('temp_c', Float(), unique=False, info={
                    'units': 'Celsius', 'units_abbrev': u'\N{DEGREE SIGN}C'})
    temp_f = Column('temp_f', Float(), unique=False, info={
                    'units': 'Fahrenheit', 'units_abbrev': u'\N{DEGREE SIGN}F'})
    uv_index = Column('uv_index', Float(), unique=False)
    wind_degrees = Column('wind_degrees', Integer(), unique=False, info={
                          'units': 'degrees', 'units_abbrev': u'\N{DEGREE SIGN}'})
    wind_dir = Column('wind_dir', String(255), unique=False)
    wind_kt = Column('wind_kt', Float(), unique=False, info={
                     'units': 'knots', 'units_abbrev': 'kn'})
    wind_mph = Column('wind_mph', Float(), unique=False, info={
                      'units': 'miles/hour', 'units_abbrev': 'mph'})
    windchill_c = Column('windchill_c', Float(), unique=False, info={
                         'units': 'Celsius', 'units_abbrev': u'\N{DEGREE SIGN}C'})
    windchill_f = Column('windchill_f', Float(), unique=False, info={
                         'units': 'Fahrenheit', 'units_abbrev': u'\N{DEGREE SIGN}F'})
