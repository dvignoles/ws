#!/bin/sh
#Run every 10 minutes

export WS_USER_ID=#WeatherLink User Id here
export WS_PASS=#WeatherLink Password here
export WS_TOKEN=#Weatherlink api token here

export WS_DB_URI=#Database URI for SQLAlchemy

export ALERT_SENDER=#Email here
export ALERT_PASS=#Email pass here
export ALERT_RECEIVER=#Email here

python run.py
