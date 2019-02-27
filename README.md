#ASRC Weather Station Website

###Set up

'cd path/to/ws
touch config.py'

populate config.py with: 

'#config.py

class Config(object):
    DEBUG = False
    TESTING = False
    DATABASE_URI = 'sqlite:///:memory:'

class ProductionConfig(Config):
    SQLALCHEMY_TRACK_MODIFICATIONS  = False
    DATABASE_URI = 'mysql://user@localhost/foo'

class DevelopmentConfig(Config):
    DEBUG = True
    TEMPLATES_AUTO_RELOAD = True

    SQLALCHEMY_TRACK_MODIFICATIONS  = False
    SQLALCHEMY_DATABASE_URI = 'sqlite:///ws.sqlite'

Edit SQLALCHEMY_DATABASE_URI with the appropriate value.

To switch between Development/Production edit __init__.py:

'app.config.from_object('config.DevelopmentConfig')'

change to:

'app.config.from_object('config.ProductionConfig')'


to run:

'export WS_SETTINGS=PATH/TO/config.py
export FLASK_APP=run.py
flask run'