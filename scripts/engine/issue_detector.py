# engine /issue_decector.py

# This module is responsible for detecting issues in the data, such as missing values and duplicates.

# looks for missing values
def detect_missing_values(df):
    return df.isnull().sum()

# looks for duplicates
def detect_duplicates(df, column_name):
    if column_name not in df.columns:
        return f"Column '{column_name}' does not exist'"
    
    return df[column_name].duplicated().sum() 


    