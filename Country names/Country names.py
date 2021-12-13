import pandas as pd
import requests

response = requests.get( "https://restcountries.com/v3.1/all" )

df = pd.DataFrame( response.json() )

df['common name'] = df['name'].apply( lambda x: x.get( 'common' ) )
df['official name'] = df['name'].apply( lambda x: x.get( 'official' ) )

my_function = lambda x: ','.join([key for key in x]) if type(x) != type( float() ) else None

df['currency'] = df['currencies'].apply( my_function )
df['language'] = df['languages'].apply( my_function )
df['capital city'] = df['capital'].apply( my_function )

df['latitude'] = df['latlng'].apply( lambda x: x[0] )
df['longitude'] = df['latlng'].apply( lambda x: x[1] )

print( df )
