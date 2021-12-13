import pandas as pd
import requests

response = requests.get( "https://restcountries.com/v3.1/all" )

df = pd.DataFrame( response.json() )

df['common name'] = df['name'].apply( lambda x: x.get( 'common' ) )
df['official name'] = df['name'].apply( lambda x: x.get( 'official' ) )

#df['currency'] = df['currencies'].apply( lambda x:  x )

print( df )
