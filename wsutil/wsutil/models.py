from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import Column, String, Integer, Float, DateTime, Date, Time


Base = declarative_base()

#WeatherLink
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

    rain_day_in = Column('rain_day_in', Float(), unique=False, info={
                         'units': 'inches', 'units_abbrev': 'in'})
    rain_rate_day_high_in_per_hr = Column('rain_rate_day_high_in_per_hr', Float(), unique=False, info={
                         'units': 'inches per hour', 'units_abbrev': 'in/hr'})
    rain_rate_hour_high_in_per_hr = Column('rain_rate_hour_high_in_per_hr', Float(), unique=False, info={
                         'units': 'inches per hour', 'units_abbrev': 'in/hr'})
    rain_rate_in_per_hr = Column('rain_rate_in_per_hr', Float(), unique=False, info={
                         'units': 'inches per hour', 'units_abbrev': 'in/hr'})
    rain_storm_in = Column('rain_storm_in', Float(), unique=False, info={
                         'units': 'inches', 'units_abbrev': 'in'})

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

#Asos
class Asos_Observation():

    #https://mesonet.agron.iastate.edu/api/
    station = Column('station', String(255), unique=False)
    name = Column('name', String(255), unique=False)
    county = Column('county', String(255), unique=False)
    state = Column('state', String(255), unique=False)
    network = Column('network', String(255), unique=False)

    local_date = Column('local_date', Date(), unique=False)

    snow = Column('snow', Float(), unique=False, info={
                        'units': '', 'units_abbrev': ''})
    snowd = Column('snowd', Float(), unique=False, info={
                        'units': '', 'units_abbrev': ''})
    snoww = Column('snoww', Float(), unique=False, info={
                        'units': '', 'units_abbrev': ''})

    utc_valid = Column('utc_valid', DateTime(), unique=True)
    local_valid = Column('local_valid', DateTime(), unique=True,primary_key=True)

    tmpf = Column('tmpf', Float(), unique=False, info={
                        'units': '', 'units_abbrev': ''})
    max_tmpf = Column('max_tmpf', Float(), unique=False, info={
                        'units': '', 'units_abbrev': ''})
    min_tmpf = Column('min_tmpf', Float(), unique=False, info={
                        'units': '', 'units_abbrev': ''})
    dwpf = Column('dwpf', Float(), unique=False, info={
                        'units': '', 'units_abbrev': ''})
    relh = Column('relh', Integer(), unique=False, info={
                        'units': '', 'units_abbrev': ''})
    sknt = Column('sknt', Integer(), unique=False, info={
                        'units': '', 'units_abbrev': ''})
    drct = Column('drct', Integer(), unique=False, info={
                        'units': '', 'units_abbrev': ''})
    gust = Column('gust', Integer(), unique=False, info={
                        'units': '', 'units_abbrev': ''})
    mslp = Column('mslp', Float(), unique=False, info={
                        'units': '', 'units_abbrev': ''})
    pres = Column('pres', Float(), unique=False, info={
                        'units': '', 'units_abbrev': ''})
    srad = Column('srad', Integer(), unique=False, info={
                        'units': '', 'units_abbrev': ''})
    phour = Column('phour', Float(), unique=False, info={
                        'units': '', 'units_abbrev': ''})
    lon = Column('lon', Float(), unique=False, info={
                        'units': '', 'units_abbrev': ''})
    lat = Column('lat', Float(), unique=False, info={
                        'units': '', 'units_abbrev': ''})
    pday = Column('pday', Float(), unique=False, info={
                        'units': '', 'units_abbrev': ''})