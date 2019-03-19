"""
    WeatherLinkScrape.py
    Author: Daniel Vignoles
    WeatherLinkScrape is a tool to scrape .xml data from api.weatherlink.com xml pages
"""

from requests import get
from requests.exceptions import RequestException
from contextlib import closing
from xml.etree import ElementTree as ET
from datetime import datetime
from bs4 import BeautifulSoup
from datetime import datetime as dt
from datetime import timedelta
from time import sleep
import smtplib
import ssl
from email.message import EmailMessage
import os

from sqlalchemy import create_engine,desc
from sqlalchemy.orm import sessionmaker
from sqlalchemy.exc import IntegrityError
from ws_models import Base, Observation


###---CONFIG---###
# ElementTree.Element name of Observation Time attribute
OBSERVATION = 'observation_time_rfc822'
# Format of parsed date to for strptime
DATE_FORMAT = '%a, %d %b %Y %H:%M:%S %z'
# Format for strftime to name files
OBSERVATION_STR = '%Y-%m-%d_%H-%M'
###------------###

CURRENT = [
    'observation_time_rfc822', 'station_name', 'dewpoint_c', 'dewpoint_f', 'heat_index_c', 'heat_index_f',
    'location', 'latitude', 'longitude', 'pressure_in', 'pressure_mb','rain_day_in','rain_rate_day_high_in_per_hr',
    'rain_rate_hour_high_in_per_hr','rain_rate_in_per_hr','rain_storm_in',
    'relative_humidity', 'solar_radiation','sunrise', 'sunset', 'temp_c', 'temp_f', 'uv_index', 'wind_degrees', 
    'wind_dir', 'wind_kt', 'wind_mph', 'windchill_c', 'windchill_f'
]


def db_record(url, Session, alert):
    """
        Record from xml url to database connection on ten minute interval
    """

    #flags
    error_count = 0
    alert_sent = False
    alert_time = None

    while True:
        session = Session()
        observation = Observation(**get_soup(url))
        
        time_of_scrape = dt.now().strftime(DATE_FORMAT)
        scraped_time = observation.datetime.strftime(DATE_FORMAT)
        last_time_in_db = session.query(Observation).order_by(desc(Observation.datetime)).first().datetime.strftime(DATE_FORMAT)

        try:
            
            session.add(observation)
            session.commit()
            print('Observation successfully recorded to database at: ', str(dt.now().strftime(DATE_FORMAT)))

            #reset flags
            error_count = 0
            alert_sent = False
            alert_time = None

        except IntegrityError:
            print('\nNo new observation found for attempt at: ', time_of_scrape)
            print('Observation time scraped from weatherlink: ', scraped_time)
            print('Last observation time recorded to database: ', last_time_in_db)
            error_count += 1
        except:
            print('Error in recording to database')
        finally:
            session.close()
            if error_count == 0:
                sleep(600)  # 10 min
            elif error_count < 7: #wait an hour before triggering alert
                print("Attemping again in 10 minutes...(",error_count,"/6)")
                sleep(600) 
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

                
                sleep(600)
                

def db_init(DB_URI):
    """
        Connect to database and return Session object
    """
    engine = create_engine(DB_URI)
    Base.metadata.create_all(engine)
    Session = sessionmaker(bind=engine)
    return(Session)


def email_alert(alert):
    content = "The Weatherlink API is currently providing an outdated observation. " + \
    "This may indicate that weather station data collection is stalled." + \
    "\n\nTime of last attempt to scrape data: " + alert['time_of_scrape'] + \
    "\n\nObservation time scraped from last attempt: " + alert['scraped_time'] + \
    "\n\nLast observation time successfully recorded to database: " + alert['last_time_in_db'] + \
    "\n\nThis alert will trigger every 12 hours until data collection can resume."

    send_email(alert['sender'],alert['pass'],alert['receivers'],'Weather Station Alert',content)


def send_email(sender, password, receivers, subject, content):
    """
        Send an email through gmail. Intended to alert admin when weather station stalls. 
    """

    msg = EmailMessage()
    msg['Subject'] = subject
    msg['From'] = sender
    msg['To'] = receivers
    msg.set_content(content)

    port = 465
    context = ssl.create_default_context()

    with smtplib.SMTP_SSL("smtp.gmail.com", port, context=context) as server:
        server.login(sender, password)

        #server.sendmail(sender, receivers, message)
        server.send_message(msg)


def get_soup(url):
    """
        Return a dictionary of the scraped CURRENT variables from url
    """

    soup = BeautifulSoup(simple_get(url), 'xml')
    observations = list(map(lambda tag: soup.find(tag), CURRENT))

    results = {}
    for obs in observations:
        tag = obs.name
        content = obs.contents[0]

        # reformat date
        if(tag == 'observation_time_rfc822'):
            dt = get_obs_time(content)

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
    date_time = get_obs_time(parse_obs_time(tree))
    year = str(date_time.year)
    month = str(date_time.month)
    day = str(date_time.day)

    path = 'data'+'/'+year+'/'+month+'/'+day

    os.makedirs(path, exist_ok=True)
    os.chdir(path)
    tree.write(get_obs_time_str(date_time)+'.xml')
    os.chdir(root_dir)


def get_obs_time_str(date_time):
    """
        Return str reprensentation in OBSERVATION_STR format of date_time
    """
    return(datetime.strftime(date_time, OBSERVATION_STR))


def get_obs_time(observation_unparsed):
    return(datetime.strptime(observation_unparsed, DATE_FORMAT))


def parse_obs_time(tree):
    """
        Return string representing the time of observation from ElementTree
    """
    return tree.getroot().find(OBSERVATION).text


def get_tree(url):
    """
        Return an ElementTree representing the XML
    """
    xml_raw = simple_get(url)
    root = ET.fromstring(xml_raw)
    tree = ET.ElementTree(root)
    return(tree)


def simple_get(url):
    """
    Attempts to get the content at `url` by making an HTTP GET request.
    If the content-type of response is some kind of JSON/XML, return the
    text content, otherwise return None.
    """
    try:
        with closing(get(url, stream=True)) as resp:
            if is_good_response(resp):
                if(is_xml(resp)):
                    return resp.content
                elif(is_json(resp)):
                    return resp.json()
            else:
                return None

    except RequestException as e:
        log_error('Error during requests to {0} : {1}'.format(url, str(e)))
        return None


def is_good_response(resp):
    """
    Returns True if the response seems to be xml, False otherwise.
    """
    content_type = resp.headers['Content-Type'].lower()
    return (resp.status_code == 200
            and content_type is not None
            and (is_xml(resp) or is_json(resp)))


def is_xml(resp):
    return resp.headers['Content-Type'].lower().find('xml') > -1


def is_json(resp):
    return resp.headers['Content-Type'].lower().find('json') > -1


def log_error(e):
    """
    Print Error
    """
    print(e)
    # TODO: Log Errors
