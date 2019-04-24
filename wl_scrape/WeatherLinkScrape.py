"""
    WeatherLinkScrape.py
    Author: Daniel Vignoles
    Purpose: Scrape XML data using the weatherlink API and organize into files or a database
"""

from datetime import datetime as dt
from datetime import timedelta
from time import sleep
import os

from sqlalchemy import desc
from sqlalchemy.exc import IntegrityError

from wsutil.utilities import get_tree, parse_xml_tag,get_datetime,get_datetime_str,get_soup,send_email
from wsutil.models import Observation,Asos_Observation,Base
from wsutil.apiwrappers import Asos

from multiprocessing import Process


###---CONFIG---#########################################

# ElementTree.Element name of Observation Time attribute
DATETIME_TAG = 'observation_time_rfc822'

# Format of parsed DATETIME_TAG to for strptime
DATETIME_FORMAT = '%a, %d %b %Y %H:%M:%S %z'

# Format for strftime to name files
DATETIME_PARSED_FORMAT = '%Y-%m-%d_%H-%M'


KEEP_TAGS = [
    'observation_time_rfc822', 'station_name', 'dewpoint_c', 'dewpoint_f', 'heat_index_c', 'heat_index_f',
    'location', 'latitude', 'longitude', 'pressure_in', 'pressure_mb','rain_day_in','rain_rate_day_high_in_per_hr',
    'rain_rate_hour_high_in_per_hr','rain_rate_in_per_hr','rain_storm_in',
    'relative_humidity', 'solar_radiation','sunrise', 'sunset', 'temp_c', 'temp_f', 'uv_index', 'wind_degrees', 
    'wind_dir', 'wind_kt', 'wind_mph', 'windchill_c', 'windchill_f'
]

###------------#########################################

def db_record(Session,wl_url,wl_alert):
    asos = Process(target=asos_record,args=(Session,))
    asos.start()
    wl = Process(target = wl_record,args=(wl_url,Session,wl_alert))
    wl.start()

    asos.join()
    wl.join()

class Asos_Jfk(Base,Asos_Observation):
    __tablename__ = 'asos_jfk'

class Asos_Nyc(Base,Asos_Observation):
    __tablename__ = 'asos_nyc'

class Asos_Lga(Base,Asos_Observation):
    __tablename__ = 'asos_lga'

class Asos_Jrb(Base,Asos_Observation):
    __tablename__ = 'asos_jrb'

def asos_record(Session):
    '''
    asos: asos apiwrapper object representing network/stations to record
    '''

    #NOAA ASOS Network/stations to record 
    stations = ['JFK','LGA','JRB','NYC']
    asos = Asos('NY_ASOS',stations)

    while True:
        session = Session()

        observations = asos.get_update()

        try:
            obs = Asos_Jfk(**observations['JFK'])
            session.add(obs)
            session.commit()
            print('JFK: Successfuly Recorded')
        except:
            print('JFK: No updates')

        try:
            obs = Asos_Nyc(**observations['NYC'])
            session.add(obs)
            session.commit()
            print('NYC: Successfuly Recorded')
        except:
            print('NYC: No updates')

        try:
            obs = Asos_Lga(**observations['LGA'])
            session.add(obs)
            session.commit()
            print('LGA: Successfuly Recorded')
        except:
            print('LGA: No updates')

        try:
            obs = Asos_Jrb(**observations['JRB'])
            session.add(obs)
            session.commit()
            print('JRB: Successfuly Recorded')
        except:
            print('JRB: No updates')

        session.close()

        print("asos_record sleeping...")
        sleep(600)

def wl_record(url, Session, alert):
    """
        Record from xml url to database connection on ten minute interval. 
            Email alerts automatically sent out if data not updating within 1 hour

        Inputs:
            url: xml url from weatherlink api
            Session: return of session_maker
                see ws_sqalch.db_init
            alert: dictionary containing 'sender', 'pass', and 'receivers'
                sender: gmail to send alerts from
                pass: password of sender gmail
                receivers: list of emails to alert
            
    """

    #flags
    error_count = 0
    alert_sent = False
    alert_time = None

    while True:
        session = Session()
        observation = Observation(**wl_soup(url))
        
        time_of_scrape = dt.now().strftime(DATETIME_FORMAT)
        scraped_time = observation.datetime.strftime(DATETIME_FORMAT)
        last_obs_in_db = session.query(Observation).order_by(desc(Observation.datetime)).first()

        if(last_obs_in_db != None): #empty database case
            last_time_in_db  = last_obs_in_db.datetime.strftime(DATETIME_FORMAT)

        #Attempt to commit scraped data url to db
        try: 
            session.add(observation)
            session.commit()
            print('Observation successfully recorded to database at: ', str(dt.now().strftime(DATETIME_FORMAT)))

            #reset flags
            error_count = 0
            alert_sent = False
            alert_time = None

        #Handle attempt to commit duplicate data
        except IntegrityError: 
            print('\nNo new observation found for attempt at: ', time_of_scrape)
            print('Observation time scraped from weatherlink: ', scraped_time)
            print('Last observation time recorded to database: ', last_time_in_db)
            error_count += 1

        #else error
        except: 
            print('Error in recording to database')

        finally:
            #Cleanup
            session.close()
            alert_time,alert_sent = error_decision(error_count,alert,alert_time,alert_sent,time_of_scrape,scraped_time,last_time_in_db)
            print('wl_record sleeping...')
            sleep(600) # 10 minutes


def error_decision(error_count,alert,alert_time,alert_sent,time_of_scrape,scraped_time,last_time_in_db):
    '''Decision making based on error_count for log / sending of email alerts'''

    if error_count == 0:
        pass

    #wait an hour before triggering alert
    elif error_count < 7: 
        print("Attemping again in 10 minutes...(",error_count,"/6)")

    #Alert cycle
    else:
        print('Weather Station Data collection offline')

        #first run
        if alert_time is not None:

            # > 12 hours since last alert
            if (dt.now() - alert_time) >= timedelta(hours=12):
                alert_sent = False

        #trigger alert, save time
        if not alert_sent:
            alert['time_of_scrape'] = time_of_scrape
            alert['scraped_time'] = scraped_time
            alert['last_time_in_db'] = last_time_in_db

            email_alert(alert)
            print("Email Alert sent to: ", alert['receivers'])
            alert_sent = True
            alert_time = dt.now()

    return((alert_time,alert_sent))


def email_alert(alert):
    '''
        Send an email concerning the weatherlink API not providing an up to date
    '''


    content = "The Weatherlink API is currently providing an outdated observation. " + \
    "This may indicate that weather station data collection is stalled." + \
    "\n\nTime of last attempt to scrape data: " + alert['time_of_scrape'] + \
    "\n\nObservation time scraped from last attempt: " + alert['scraped_time'] + \
    "\n\nLast observation time successfully recorded to database: " + alert['last_time_in_db'] + \
    "\n\nThis alert will trigger every 12 hours until data collection can resume."

    send_email(alert['sender'],alert['pass'],alert['receivers'],'Weather Station Alert',content)

def wl_soup(url):
    """
        Return a dictionary of the scraped KEEP_TAGS variables from url
    """

    observations = get_soup(url,KEEP_TAGS)

    results = {}
    for obs in observations:
        tag = obs.name
        content = obs.contents[0]

        # reformat date
        if(tag == DATETIME_TAG):
            dt = get_datetime(content,DATETIME_FORMAT)

            results['datetime'] = dt

            results['date'] = dt.date()

            results['time'] = dt.time()

            tz = dt.tzinfo.tzname(dt)
            results['timezone'] = tz
        else:
            try:
                results[tag] = int(content)
            except ValueError:
                try:
                    results[tag] = float(content)
                except:
                    results[tag] = content

    return results


def write_xml(url):
    """
        url: api.weatherlink.com xml webpage
        write_xml writes a .xml to data folder in the appropriate year/month/day/ path
    """
    root_dir = os.getcwd()

    tree = get_tree(url)
    date_time = get_datetime(parse_xml_tag(tree,DATETIME_TAG),DATETIME_FORMAT)
    year = str(date_time.year)
    month = str(date_time.month)
    day = str(date_time.day)

    path = 'data'+'/'+year+'/'+month+'/'+day

    os.makedirs(path, exist_ok=True)
    os.chdir(path)
    tree.write(get_datetime_str(date_time,DATETIME_PARSED_FORMAT)+'.xml')
    os.chdir(root_dir)