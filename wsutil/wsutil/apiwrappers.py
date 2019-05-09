from .utilities import simple_get
from .models import Asos_Observation

from datetime import datetime
class Noaav2:
    #TODO:make this funcitonal
    HEADER = {'token':'TOKEN HERE'}

    base_url = 'https://www.ncdc.noaa.gov/cdo-web/api/v2/'

    'https://www.ncdc.noaa.gov/cdo-web/api/v2/data?datasetid=GHCND&stationid=72505394728&72506094728&99999994728&startdate=2019-01-01&enddate=2019-03-04'

    x = simple_get('https://www.ncdc.noaa.gov/cdo-web/api/v2/locationcategories',headers=HEADER)

class Asos:

    def __init__(self,network,stations):
        self.network = network
        self.url = 'https://mesonet.agron.iastate.edu/geojson/network_obs.php?network='+ network
        self.stations = stations
    
    def __request(self):
        return(simple_get(self.url))

    def get_update(self):
        #NOTE: This Api only gets hourly Updates
        json = self.__request()

        if json == None:
            raise RuntimeError('None received from web request for {}'.format(self.network))

        update = {}
        for feature in json['features']: 
            station_id = feature['id']
            if station_id not in self.stations:
                continue
            properties = feature['properties']

            #datetime conversion
            properties['local_date'] = datetime.strptime(properties['local_date'],'%Y-%m-%d').date()
            properties['utc_valid'] = datetime.strptime(properties['utc_valid'],'%Y-%m-%dT%H:%M:%SZ')
            properties['local_valid'] = datetime.strptime(properties['local_valid'],'%Y-%m-%dT%H:%M:%S')

            keep_vars = vars(Asos_Observation).keys()
            for key in list(properties.keys()):
                if key not in keep_vars:
                    del properties[key]



            update[station_id] = properties
        
        return(update)

        #TODO: Use OTHER Api 5-minute Resolution
        #NOTE: 5 minute observations do not contain as much detail as hourly obs
        '''https://mesonet.agron.iastate.edu/cgi-bin/request/asos.py?
        station=JFK&station=JRB&station=LGA&station=NYC&
        data=tmpf&data=tmpc&data=dwpf&data=dwpc&data=relh&data=feel&data=drct&data=sknt&data=sped&data=mslp&data=p01m&data=p01i&data=gust&data=gust_mph&data=peak_wind_gust&data=peak_wind_gust_mph&data=peak_wind_drct&data=peak_wind_time
        &year1=2019&month1=4&day1=24&year2=2019&month2=4&day2=24&tz=America%2FNew_York
        &format=onlycomma
        &latlon=yes
        &trace=empty
        &direct=no
        '''