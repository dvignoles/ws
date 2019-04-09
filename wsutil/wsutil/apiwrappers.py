from .utilities import simple_get

class Noaav2:
    #TODO:make this funcitonal
    HEADER = {'token':'TOKEN HERE'}

    base_url = 'https://www.ncdc.noaa.gov/cdo-web/api/v2/'

    'https://www.ncdc.noaa.gov/cdo-web/api/v2/data?datasetid=GHCND&stationid=72505394728&72506094728&99999994728&startdate=2019-01-01&enddate=2019-03-04'

    x = simple_get('https://www.ncdc.noaa.gov/cdo-web/api/v2/locationcategories',headers=HEADER)

class Asos:

    def __init__(self,network):
        self.network = network
        self.url = 'https://mesonet.agron.iastate.edu/geojson/network_obs.php?network='+ network
    
    def request(self):
        return(simple_get(self.url))

    def get_update(self):
        json = self.request()
        stations = []
        for feature in json['features']:
            properties = feature['properties']
            properties['coordinates'] = feature['geometry']['coordinates']
            stations.append(properties)
            return(stations)