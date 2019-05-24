"""
    run.py
    Author: Daniel Vignoles

    Purpose: Scrape the contents of an api.weather.com xml page to database
"""

from WeatherLinkScrape import db_record
import os
import configparser

config = configparser.ConfigParser()
config.read('../config.ini')

username =  config['WEATHERLINK']['id'] 
password = config['WEATHERLINK']['password'] 
token = config['WEATHERLINK']['token'] 

XML_URL = 'https://api.weatherlink.com/v1/NoaaExt.xml?user=' + \
    username + '&pass=' + password + '&apiToken=' + token

alerts = {'sender':config['ALERTS']['sender'],'pass':config['ALERTS']['sender_password'],'receivers':config['ALERTS']['receivers']}

db_record(config['DATABASE']['dev'],XML_URL,alerts)
#change dev to prod to switch databases 