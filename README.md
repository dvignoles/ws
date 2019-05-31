
# ASRC Weather Station Data Collection and Website

## About

In late 2018/early 2019 a personal weather station was installed on the rooftop of the [CUNY Advanced Science Research Center](https://asrc.gc.cuny.edu/). This project collects the data from the ASRC station and three other NYC weather stations available on [NOAA'S ASOS Network](https://www.ncdc.noaa.gov/data-access/land-based-station-data/land-based-datasets/automated-surface-observing-system-asos). 

The data is displayed in a flask application with a backend database. Check out the site at https://asrcweather.environmentalcrossroads.org/

## Requirements / Dependencies
```
#create virtual environment
cd path/to/ws
python -m venv env
source env/bin/activate

#install wsutil package
cd wsutil
pip install . 

#other dependencies
cd ..
pip install -r requirements.txt
```
## Configuration
This project relies on a 'config.ini' file located at the root of the project. You can generate a skeleton for this file:

```
python ws/config_gen.py
```

Then edit config.ini with the appropriate values:

```
[DATABASE]
dev = sqlite://
prod = sqlite://

[WEATHERLINK]
id = example_id
password = example_password
token = token123

[ALERTS]
sender = example@email.com
sender_password = mypassword
receivers = example1@email.com,example2@email.com

[WEB]
secret_key = you-will-never-guess
port = 5000
host = 0.0.0.0

```
`[DATABASE]` should reference [Sqlalchemy Database Urls](https://docs.sqlalchemy.org/en/13/core/engines.html)

`[WEATHERLINK]` should your reference your personal [Weatherlink API Information](https://www.weatherlink.com/static/docs/APIdocumentation.pdf)

`[ALERTS]` contains account information for an email alert service that triggers should data collection stall. The sender account should be a gmail account with secure login disabled. 

`[WEB]` defines deployment options for the flask server. 

**Finally, define an environment variable with the location of config.ini**

`export WS_CONFIG=/path/to/config.ini`
## wl_scrape Module
The wl_scrape module collects data from the ASRC Weather Station and ASOS Network via their respective API. Data is organized in a database using SQLAlchemy.

To switch between development and production database configurations edit `wl_scrape/run.py`

Dev: `db_record(config['DATABASE']['dev'],XML_URL,alerts)`

Prod: `db_record(config['DATABASE']['prod'],XML_URL,alerts)`

The production version of this module is implemented as a Linux systemd service. 

## web Module

The web module is a flask web application intended to interface with the database maintained by wl_scrape. 

Flask specific configuration options for dev/prod are defined in `web/config.py`

```
#config.py

class Config(object):
    DEBUG = False
    TESTING = False
    DATABASE_URI = 'sqlite:///:memory:'
    SECRET_KEY = config['WEB']['secret_key']
    TEMPLATES_AUTO_RELOAD = True


class ProductionConfig(Config):
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    SQLALCHEMY_DATABASE_URI = config['DATABASE']['prod']


class DevelopmentConfig(Config):
    DEBUG = True
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    SQLALCHEMY_DATABASE_URI = config['DATABASE']['dev']

```

To switch between ProductionConfig and DevelopmentConfig edit `web/app/__init__.py`

```
#Flask Config
app.config.from_object('config.DevelopmentConfig')
```

```
#Flask Config
app.config.from_object('config.ProductionConfig')
```

To run the test server:

```
cd web
export FLASK_APP=run.py
flask run
```

The production WSGI of this module is implemented as a Linux systemd service.
