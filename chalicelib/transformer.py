import pandas as pd

class DataFrameTransformer:
    def __init__(self):
        return
    def getPercOfDiffDf(self, df1, df2, idxColumns):
        resDf = df1.copy()
        idxColumns = set(idxColumns)
        columns = list(df1.columns)
        for col in columns:
            if col in idxColumns:
                continue
            resDf[col] = abs(df1[col] - df2[col]) / ((df1[col] + df2[col]//2)) * 100
        return resDf.round(2)

    