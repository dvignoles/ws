#ASRC Weather Station Website

###Set up

To link your database create a config.py file and define:
    SQLALCHEMY_DATABASE_URI = 'sqlite:////ws.sqlite'
export WS_SETTINGS=PATH/TO/CONFIG.py
export FLASK_APP=run.py
flask run