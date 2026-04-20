# This script accepts a csv file from the command line and saves it in raw data folder.
import argparse
from pathlib import Path
from scripts.engine.csv_parser import load_csv                                     
from scripts.engine.schema_inference import infer_schema, dtype_mapping   
from scripts.engine.cleaner import clean_data, handle_nulls, drop_high_null_columns, handle_outliers
from scripts.engine.analyzer import analyze
from scripts.engine.outliers import detect_outliers

def main():
    parser = argparse.ArgumentParser(description='Load a CSV file')
    parser.add_argument('input_file', help='Path to input CSV')
    args = parser.parse_args()

    # Load the CSV into a DataFrame and print the first few rows to verify
    df = load_csv(args.input_file)
    if df is not None:
        print(df.head())

        schema = infer_schema(df)
        print("\nInferred Schema:")
        for column, dtype in schema.items():
            print(f"{column}: {dtype}")

        mismatches = dtype_mapping(df, schema)
        print(mismatches)
        print("\nData Type Mismatches:")
        for column, values in mismatches.items():
            print(f"{column}: Expected={values['expected']}, Actual={values['actual']}")

        df = clean_data(df, schema)
        print(df.dtypes)

        print("\nColumn summary")
        summary = analyze(df)
        for col, info in summary.items():                                                                                                                                                                                    
            print(f"{col}: dtype={info['dtype']}, nulls={info['nulls']}, non-nulls={info['non-nulls']}")

        print("\nOutliers:")
        outliers = detect_outliers(df, schema)
        for col, outlier_rows in outliers.items():
            print(f"\n{col}: {len(outlier_rows)} outliers detected")   #get the count
            print(outlier_rows[[col]]) # print the actual values of the outliers

        print("\nHandling outliers...")
        df = handle_outliers(df, schema)


        print("\nDropping columns with high null percentages...")
        df = drop_high_null_columns(df, threshold=0.5)
        for col in df.columns:
            print(f"{col}: {df[col].isnull().sum()} nulls")

        print("\nAfter handling null values:")
        df = handle_nulls(df, schema)
        summary = analyze(df)
        for col, info in summary.items():                                                                                                                                                                                    
            print(f"{col}: dtype={info['dtype']}, nulls={info['nulls']}, non-nulls={info['non-nulls']}")

    input_path = Path(args.input_file)
    output_path = Path("data/cleaned") / (input_path.stem + '_cleaned.csv')               
    df.to_csv(output_path, index=False)
    print(f"\nCleaned data saved to: {output_path}")     
    
if __name__ == '__main__':
    main()



