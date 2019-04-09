
# ASRC Weather Station Data Collection and Website

## Requirements / Dependencies
```
#install wsutil package
cd wsutil
pip install . 

#other dependencies
cd ..
pip install -r requirements.txt

```

## wl_scrape Module

The wl_scrape module collects data from the ASRC Weather Station using the Weatherlink API. Data is organized in database using SQLAlchemy. 

## web Module

The web module is a flask web application intended to interface with the database mainted by wl_scrape. 

## Environment Variables

This project uses environement variables for configuration. Add these to your .bash_profile or export in a custom startup script.

```
#Weather Station Project

#Databases
export DEV_URI=#DEVELOPMENT DATABASE URL HERE
export PROD_URI=#PRODUCTION DATABASE URL HERE

#Weatherlink
export WS_USER_ID=#WEATHERLINK ID HERE
export WS_PASS=#WEATHERLINK PASSWORD HERE
export WS_TOKEN=#WEATHERLINK API TOKEN HERE

#Alerts
export ALERT_SENDER=#me@example.com
export ALERT_PASS=#my@example.com's password
export ALERT_RECEIVERS=you@example.com,you2@example.com

```
#### TODO: Explore better configuration option and method of switching from DEV/PROD URI
