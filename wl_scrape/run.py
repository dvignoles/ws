"""
    run.py
    Author: Daniel Vignoles

    Purpose: Scrape the contents of an api.weather.com xml page to database
"""

from WeatherLinkScrape import db_init, db_record
import os

username = os.environ['WS_USER_ID']
password = os.environ['WS_PASS']
token = os.environ['WS_TOKEN']

XML_URL = 'https://api.weatherlink.com/v1/NoaaExt.xml?user=' + \
    username + '&pass=' + password + '&apiToken=' + token

Session = db_init(os.environ['DEV_URI']) #Change to 'PROD_URI' to use Production Database

#alert_receivers = list(os.environ['ALERT_RECEIVERS'].split(','))
alerts = {'sender':os.environ['ALERT_SENDER'],'pass':os.environ['ALERT_PASS'],'receivers':os.environ['ALERT_RECEIVERS']}

db_record(XML_URL, Session,alerts)
