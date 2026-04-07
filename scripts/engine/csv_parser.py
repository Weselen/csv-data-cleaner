# engine/csv_parser.py

# this module is responsible for loading CSV files and standardizing column names. 
# It uses pandas for data manipulation and includes a function to clean column names by removing whitespace, 
# replacing spaces with underscores, splitting camelCase, converting to lowercase, and removing special characters.

import pandas as pd
import re

# Data standardization: clean column names, remove whitespace, replace spaces with underscores, 
# split camelCase, convert to lowercase, and remove special characters
def clean_column_names(column_name):
    # Remove leading/trailing whitespace
    column_name = column_name.strip()

    # Replace spaces with underscores
    column_name = re.sub(r'\s+', '_', column_name)

    # Split camelCase / PascalCase
    column_name = re.sub(r'([a-z0-9])([A-Z])', r'\1_\2', column_name)

    # Convert to lowercase
    column_name = column_name.lower()

    # Remove special characters except underscore
    column_name = re.sub(r'[^\w_]', '', column_name)

    return column_name


def load_csv(file_path):
    """
    Load a CSV file into a pandas DataFrame and standardize column names.
    """
    try:
        df = pd.read_csv(file_path) 
    except Exception as e:
        print(f"Error loading CSV file: {e}")
        return None
    
    df.columns = [clean_column_names(col) for col in df.columns]
    return df
