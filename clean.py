# This script accepts a csv file from the command line and saves it in raw data folder.
import argparse
import json
from pathlib import Path
from scripts.engine.csv_parser import load_csv                                     
from scripts.engine.schema_inference import infer_schema  
from scripts.engine.cleaner import clean_data, handle_nulls, drop_high_null_columns, handle_outliers


def main():
    parser = argparse.ArgumentParser(description='Load a CSV file')
    parser.add_argument('input_file', help='Path to input CSV')
    args = parser.parse_args()

    # Load profiles.json to get the expected schema for the data. This will be used for cleaning and handling nulls.
    
    with open('data/profiles.json', 'r') as file:
        choices = json.load(file)
        for each in choices:
            print(each)
        profile_name = input("Enter the profile name to use for cleaning: ")
        null_rules = choices.get(profile_name)
        if null_rules is None:
            print(f"Profile '{profile_name}' not found. Exiting.")
            return


    # Load the CSV into a DataFrame and print the first few rows to verify
    df = load_csv(args.input_file)
    if df is not None:
        schema = infer_schema(df)
        df = clean_data(df, schema)
        df = handle_outliers(df, schema)
        df = drop_high_null_columns(df, threshold=0.5)
        df = handle_nulls(df, schema, null_rules)
    if df is None:
        return  

    input_path = Path(args.input_file)
    output_path = Path("data/cleaned") / (input_path.stem + '_cleaned.csv')   
    output_path.parent.mkdir(parents=True, exist_ok=True)             
    df.to_csv(output_path, index=False) 
    print(f"\nCleaned data saved to: {output_path}")     
    
if __name__ == '__main__':
    main()



