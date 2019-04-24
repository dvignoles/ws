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
        json = self.__request()
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