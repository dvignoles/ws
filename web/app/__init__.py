# app/__init__.py
from flask import Flask
from flask_sqlalchemy import SQLAlchemy
import os
import sys
import configparser
from wsutil.models import Observation

# Initialize the app
app = Flask(__name__, instance_relative_config=True)

#Project Config
config = configparser.ConfigParser()
config.read('../config.ini')

# Flask Config
app.config.from_object('config.DevelopmentConfig')

# Database
db = SQLAlchemy(app)
db.reflect(app=app)

# Load the views
from app import views
