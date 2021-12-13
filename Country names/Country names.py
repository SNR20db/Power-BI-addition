import pandas as pd
import requests

response = requests.get( "https://restcountries.com/v3.1/all" )

df = pd.DataFrame( response.json() )

df['common name'] = df['name'].apply( lambda x: x.get( 'common' ) )
df['official name'] = df['name'].apply( lambda x: x.get( 'official' ) )

my_function = lambda x: ','.join([key for key in x]) if type(x) != type( float() ) else None
my_function_value = lambda x: ','.join([value for key, value in x]) if type(x) != type( float() ) else None

df['currency'] = df['currencies'].apply( my_function )
df['language'] = df['languages'].apply( my_function )
df['capital city'] = df['capital'].apply( my_function )
df['border'] = df['borders'].apply( my_function )

df['latitude'] = df['latlng'].apply( lambda x: x[0] )
df['longitude'] = df['latlng'].apply( lambda x: x[1] )

df['demonym f'] = df['demonyms'].apply( lambda x: x.get( 'eng' ).get( 'f' ) if type(x) != type( float() ) else None )
df['demonym m'] = df['demonyms'].apply( lambda x: x.get( 'eng' ).get( 'm' ) if type(x) != type( float() ) else None )

df['google maps link'] = df['maps'].apply( lambda x: x.get( 'googleMaps' ) )

df['gini year'] = df['gini'].apply( my_function )
df['gini value'] =  df['gini'].apply( lambda x: ','.join( [ str( value ) for value in list( x.values() ) ] ) if type(x) != type( float() ) else None )

df['car side'] = df['car'].apply( lambda x: x.get( 'side' )  )

df['time zones'] = df['timezones'].apply( lambda x: ','.join(x) )

df['continent'] = df['continents'].apply (lambda x: ','.join(x) )

print( df )
