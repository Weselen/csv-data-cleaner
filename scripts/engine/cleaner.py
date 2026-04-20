import pandas as pd

# This module contains functions for cleaning and preprocessing data

NULL_RULES = {
      "numeric": "median",                                                                                                                                             
      "string": "unknown",                                                                                                                                           
      "boolean": False,                                                                                                                                                
      "datetime": "drop",                                                                                                                                            
      "id": "drop",                                                                                                                                                    
  }


# Handles cleaning of data based on the inferred schema, such as converting datatypes. 
def clean_data(df, schema):
    # Check for Datetime columns and convert them to datetime format
    for column in df.columns:
        expected_type = schema.get(column)
        if expected_type == "datetime":
            df[column] = pd.to_datetime(df[column], errors='coerce')  # Convert to datetime, coerce errors to NaT
        elif expected_type == "numeric":
            df[column] = pd.to_numeric(df[column], errors='coerce')  # Convert to numeric, coerce errors to NaN
    return df

# Handle null values by filling them with appropriate defaults based on the inferred schema
def handle_nulls(df, schema):
    for column in df.columns:
        null_value = schema.get(column) # get the type of null value
        rule = NULL_RULES.get(null_value)
        if rule == "median":
            df[column] = df[column].fillna(df[column].median())
        elif rule == "unknown":
            df[column] = df[column].fillna("Unknown")
        elif rule is False:
            df[column] = df[column].fillna(False)
        elif rule == "drop":
            df = df.dropna(subset=[column])

    return df

# Flag columns with high null percentages and drop them if they exceed a certain threshold (e.g., 50%)
def drop_high_null_columns(df, threshold=0.5):
    for column in df.columns:
        null_count = df[column].isnull().sum()# number of nulls in the column
        if null_count / len(df) > threshold: # divide by total number of rows to get percentage
            df = df.drop(column, axis=1) # drop the column.  axis=1 indicates we are dropping a column, not a row   
    return df


# Handle outliers by capping them to a certain threshold based on the IQR method
def handle_outliers(df, schema):
    for column in df.columns:
        expected_type = schema.get(column)
        if expected_type == "numeric":
            Q1 = df[column].quantile(0.25)
            Q3 = df[column].quantile(0.75)
            IQR = Q3 - Q1
            lower = Q1 - 1.5 * IQR
            upper = Q3 + 1.5 * IQR
            df[column] = df[column].clip(lower, upper) # cap the values to the lower and upper bounds
    return df
