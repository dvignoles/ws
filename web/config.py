#config.py
import os

class Config(object):
    DEBUG = False
    TESTING = False
    DATABASE_URI = 'sqlite:///:memory:'

class ProductionConfig(Config):
    SQLALCHEMY_TRACK_MODIFICATIONS  = False
    SQLALCHEMY_DATABASE_URI = os.environ['PROD_URI']

class DevelopmentConfig(Config):
    DEBUG = True
    TEMPLATES_AUTO_RELOAD = True

    SQLALCHEMY_TRACK_MODIFICATIONS  = False
    SQLALCHEMY_DATABASE_URI = os.environ['DEV_URI']