import pandas as pd
import requests as r

res=pd.DataFrame(pd.json_normalize(r.get("https://restcountries.eu/rest/v2/all").json()))

print(res)

