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
from os import getcwd,chdir,makedirs
from bs4 import BeautifulSoup
import smtplib, ssl


###---CONFIG---###
#ElementTree.Element name of Observation Time attribute
OBSERVATION = 'observation_time_rfc822'
#Format of parsed date to for strptime
DATE_FORMAT = '%a, %d %b %Y %H:%M:%S %z'
#Format for strftime to name files
OBSERVATION_STR = '%Y-%m-%d_%H-%M'
###------------###

CURRENT = [
    'observation_time_rfc822','station_name','dewpoint_c','dewpoint_f','heat_index_c','heat_index_f',
    'location','latitude','longitude','pressure_in','pressure_mb','relative_humidity','solar_radiation',
    'sunrise','sunset','temp_c','temp_f','uv_index','wind_degrees','wind_dir','wind_kt','wind_mph',
    'windchill_c','windchill_f'
]

def send_email(sender,password,receiver,message):
    """
        Send an email through gmail. Intended to alert admin when weather station stalls. 
    """
    port = 465
    context = ssl.create_default_context()

    with smtplib.SMTP_SSL("smtp.gmail.com", port, context=context) as server:
        server.login(sender, password)
        server.sendmail(sender, receiver, message)

def get_soup(url):
    """
        Return a dictionary of the scraped CURRENT variables from url
    """

    soup = BeautifulSoup(simple_get(url),'xml')
    observations = list(map(lambda tag:soup.find(tag),CURRENT))

    results = {}
    for obs in observations:
        tag = obs.name
        content = obs.contents[0]

        #reformat date
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
    root_dir = getcwd()

    tree = get_tree(url)
    date_time = get_obs_time(parse_obs_time(tree))
    year = str(date_time.year)
    month = str(date_time.month)
    day = str(date_time.day)

    path = 'data'+'/'+year+'/'+month+'/'+day

    makedirs(path,exist_ok=True)
    chdir(path)
    tree.write(get_obs_time_str(date_time)+'.xml')
    chdir(root_dir)

def get_obs_time_str(date_time):
    """
        Return str reprensentation in OBSERVATION_STR format of date_time
    """
    return(datetime.strftime(date_time,OBSERVATION_STR))

def get_obs_time(observation_unparsed):
    return(datetime.strptime(observation_unparsed,DATE_FORMAT))

def parse_obs_time(tree):
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
    #TODO: Log Errors


