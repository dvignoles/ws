# app/__init__.py

from flask import Flask
from flask_sqlalchemy import SQLAlchemy
import os,sys

#Observation Class from wl_scrape one directory up
sys.path.append(os.path.join(os.path.dirname(sys.path[0]),'wl_scrape'))
from wl_sqlalch import Observation

# Initialize the app
app = Flask(__name__, instance_relative_config=True)

# Load the config file
app.config.from_object('config.DevelopmentConfig')

#Database
db = SQLAlchemy(app)
db.reflect(app=app)

# Load the views
from app import views