'''
A spot for miscelaneous testing without all the fuss of running the flask instance
'''

from wsutil.sqlalch import db_init
from wsutil.models import Observation
from datetime import datetime
from queries import asrc_date_range,asrc_records
import configparser

from sqlalchemy.sql import select
import pandas
import plotly
import plotly.plotly as py
import plotly.graph_objs as go
import json
import os
import plotly.offline as offline

config = configparser.ConfigParser()
config.read(os.environ['WS_CONFIG'])
Session = db_init(config['DATABASE']['dev'])
session = Session()
