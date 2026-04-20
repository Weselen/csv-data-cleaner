import pandas as pd
import numpy as np

# function takes a dataframe and returns the dtype, nuls and not nulls and returns the sum
def analyze(df): 
    summary = {}
    for column in df.columns:
        not_null = df.notnull().sum()[column]
        is_null = df.isnull().sum()[column]
        dtypes = df.dtypes[column]
        summary[column] = {
            "column": column,
            "dtype": dtypes,
            "nulls": is_null,
            "non-nulls": not_null
        }
    return summary
