"""
    run.py
    Author: Daniel Vignoles

    Purpose: Scrape the contents of an api.weather.com xml page to data directory
"""

from WeatherLinkScrape import write_xml
from wl_sqlalch import db_init,db_record
import os

username = os.environ['WS_USER_ID']
password = os.environ['WS_PASS']
token = os.environ['WS_TOKEN']

XML_URL = 'https://api.weatherlink.com/v1/NoaaExt.xml?user='+ username +'&pass=' + password +'&apiToken=' + token

conn = db_init(os.environ['WS_DB_URI'])
db_record(XML_URL,conn)