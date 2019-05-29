# config.py
import os
from app import config

class Config(object):
    DEBUG = False
    TESTING = False
    DATABASE_URI = 'sqlite:///:memory:'
    SECRET_KEY = config['WEB']['secret_key']
    TEMPLATES_AUTO_RELOAD = True


class ProductionConfig(Config):
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    SQLALCHEMY_DATABASE_URI = config['DATABASE']['prod'] #os.environ['PROD_URI']


class DevelopmentConfig(Config):
    DEBUG = True
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    SQLALCHEMY_DATABASE_URI = config['DATABASE']['dev'] #os.environ['DEV_URI']
