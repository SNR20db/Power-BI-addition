import requests as r
import pandas as pd
import gzip

bulkdata=gzip.decompress(r.get("https://bulk.meteostat.net/v2/stations/full.json.gz").content)

stations=pd.DataFrame(pd.json_normalize(bulkdata))

print(stations)