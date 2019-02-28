# ASRC Weather Station Data Collection and Website

This project contains two modules intended to be used with one another. 

## wl_scrape Module

The wl_scrape module collects data from the ASRC Weather Station using the Weatherlink API. Data is organized in database using SQLAlchemy. 

## web Module

The web module is a flask web application intended to interface with the database mainted by wl_scrape. 
