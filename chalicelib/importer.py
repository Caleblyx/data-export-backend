from urllib.request import Request, urlopen
import json
import pandas as pd

class DataFrameImporter:
    def __init__(self, url):
        req = Request(url, headers={'User-Agent': 'Mozilla/5.0'})
        jsonString = urlopen(req).read()
        result = json.loads(jsonString)["result"]
        columns = list(pd.json_normalize(result["fields"])["id"])
        self.df = pd.json_normalize(result['records'])[columns]
        for col in columns:
            if col != "sex":
                self.df[col] = self.df[col].replace('-', pd.NA)
                self.df[col] = pd.to_numeric(self.df[col])
    
    def getDataFrame(self):
        return self.df
    
    def getFilteredDataFrame(self, col, value):
        df = self.df[self.df[col] == value]
        df.reset_index(drop=True, inplace=True)
        return df

