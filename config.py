#config.py

#Enable Flask's debugging features. Should be false in production
DEBUG = True
TEMPLATES_AUTO_RELOAD = True
SQLALCHEMY_DATABASE_URI = 'sqlite:///ws.sqlite'
SQLALCHEMY_TRACK_MODIFICATIONS  = False