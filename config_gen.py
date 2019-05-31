'''Generate a config.ini file with placeholder values'''

import configparser
config = configparser.ConfigParser()

config['DATABASE'] = {'dev_url': 'sqlite://','prod_url':'sqlite://'}
config['WEATHERLINK'] = { 'id':'example_id','password':'example_password','token':'token123'}
config['DATABASE'] = {'dev': 'sqlite://','prod':'sqlite://'}
config['ALERTS'] = {'sender':'example@email.com','sender_password':'mypassword','receivers':'example1@email.com,example2@email.com'}
config['WEB'] = {'secret_key':'you-will-never-guess','PORT':'5000','HOST':'0.0.0.0'}

with open('config.ini','w') as myconfig:
    config.write(myconfig)