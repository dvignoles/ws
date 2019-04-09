from utilities import simple_get

HEADER = {'token':'sARcTkcudgSlfzgkfbHEFlgBouESYOiF'}

base_url = 'https://www.ncdc.noaa.gov/cdo-web/api/v2/'

'https://www.ncdc.noaa.gov/cdo-web/api/v2/data?datasetid=GHCND&stationid=72505394728&72506094728&99999994728&startdate=2019-01-01&enddate=2019-03-04'

x = simple_get('https://www.ncdc.noaa.gov/cdo-web/api/v2/locationcategories',headers=HEADER)