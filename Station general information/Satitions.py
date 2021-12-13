
import os
import csv
import json
import gzip

import requests
from requests.exceptions import HTTPError

import pandas

ENDPOINT = '//bulk.meteostat.net/v2/'

HOURLY_CSV_DATA_HEADER = ('id', 'date', 'hour', 'temp', 'dwpt', 'rhum', 'prcp', 'snow', 'wdir', 'wspd', 'wpgt', 'pres', 'tsun', 'coco')
DAILY_CSV_DATA_HEADER = ('id', 'date', 'tavg', 'tmin', 'tmax', 'prcp', 'snow', 'wdir', 'wspd', 'wpgt', 'pres', 'tsun')
MONTHLY_CSV_DATA_HEADER = ('id', 'year', 'month', 'tavg', 'tmin', 'tmax', 'prcp', 'snow', 'wdir', 'wspd', 'wpgt', 'pres', 'tsun')
NORMALS_CSV_DATA_HEADER = ('id', 'star', 'end', 'month', 'tmin', 'tmax', 'prcp', 'wspd', 'pres', 'tsun')

class OptionsManager(object):
    """Class for option managment"""

    def __init__(self) -> None:

        self.api_version='0'
        self.use_https=True

        proxies={
            'http': os.environ.get('http_proxy', None),
            'https': os.environ.get('https_proxy', None)
        }

        self.requests={'proxies': proxies}

    def __str__(self) -> str:
        return "Endpoint: {}, Use https: {}".format(
            ENDPOINT, self.use_https
        )

    def __repr__(self) -> str:
        return self.__str__()

#    def __getattribute__(self, name: str) -> Any:
#        return super().__getattribute__(name)
    
#    def __setattr__(self, name: str, value: Any) -> None:
#        return super().__setattr__(name, value)

options=OptionsManager()

def _get_endpoint_url() -> str:
    """Create the endpoint url."""

    components = {"http": "https:" if options.use_https else "http:",
        "endpoint": ENDPOINT
    }

    return "{http}{endpoint}".format(**components)

def _get_data_from_endpoint(url:str = None, isstation:bool = True, station:str = None, **kwargs) -> str:
    """Gets data from the stablished endpoint."""
    result = []
    
    try:
        response = requests.get(url)

        response.raise_for_status()
    except HTTPError as http_err:
        print('Invalid request. Code: {}, reason: {}, text: {}'.format(
            response.status_code, response.reason, response.text
            )
        )

        pass
    else:
        data = gzip.decompress(response.content)

        my_string = data.decode('utf-8')

        if isstation == True:
            for line in my_string.splitlines():
                result.append(
                    '{},{}'.format(station,line)
                    )
            
            return result
        
        return my_string

def _get_json_from_csv(data:str = None, fieldnames:tuple = None, **kwargs) -> json:
    """Parses data from csv to json dict."""
    result = []

    reader = csv.DictReader(data, fieldnames=fieldnames, delimiter=',', lineterminator='\r\n')

    for row in reader:
        result.append(row)

    return json.dumps(result)

def get_stations_full(**kwargs) -> json:
    """retrieves station full information.
    Parameters
    ----------
    **kwargs :
        Optional arguments that ``requests.get()`` takes. For example,
        `proxies`, `cert` and `verify`.
    
    Returns
    -------
    json
        the requested data.
    See: 
    
        https://dev.meteostat.net/bulk/stations.html#endpoints
    
    for more details"""

    endpoint = _get_endpoint_url()

    components={
        "action": "stations/full.json.gz"
    }

    url = "{}{action}".format(endpoint, **components)

    response = _get_data_from_endpoint(url=url, isstation=False, station=None)

    return json.loads(response)

data = get_stations_full()

df = pandas.DataFrame(data)

my_function = lambda x: json.loads(str(x).replace( '\'', '\"' )) 


df['name'] = df['name'].apply( lambda x: x.get( 'en' ) )

df['model start'] = df['inventory'].apply( lambda x: x.get( 'model' ).get( 'start' ) )
df['model end'] = df['inventory'].apply( lambda x: x.get( 'model' ).get( 'end' ) )

df['hourly start'] = df['inventory'].apply( lambda x: x.get( 'hourly' ).get( 'start' ) )
df['hourly end'] = df['inventory'].apply( lambda x: x.get( 'hourly' ).get( 'end' ) )

df['daily start'] = df['inventory'].apply( lambda x: x.get( 'daily' ).get( 'start' ) )
df['daily end'] = df['inventory'].apply( lambda x: x.get( 'daily' ).get( 'end' ) )

df['monthly start'] = df['inventory'].apply( lambda x: str( x.get( 'monthly' ).get( 'start' ) ) )
df['monthly end'] = df['inventory'].apply( lambda x: str( x.get( 'monthly' ).get( 'end' ) ) )

df['normals start'] = df['inventory'].apply( lambda x: str( x.get( 'normals' ).get( 'start' ) ) )
df['normals end'] = df['inventory'].apply( lambda x: str( x.get( 'normals' ).get( 'end' ) ) )

df['identifier national'] = df['identifiers'].apply( lambda x: str( x.get( 'national' ) ) )
df['identifier wmo'] = df['identifiers'].apply( lambda x: str( x.get( 'wmo' ) ) )
df['identifier icao'] = df['identifiers'].apply( lambda x: str( x.get( 'icao' ) ) )

df['latitude'] = df['location'].apply( lambda x: str( x.get( 'latitude' ) ) )
df['longitude'] = df['location'].apply( lambda x: str( x.get( 'longitude' ) ) )
df['elevation'] = df['location'].apply( lambda x: str( x.get( 'elevation' ) ) )

print( df )
