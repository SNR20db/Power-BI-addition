import pandas as pd
import requests as r

res=r.get("https://restcountries.eu/rest/v2/all")

res=pd.DataFrame(res.json())

print(res)