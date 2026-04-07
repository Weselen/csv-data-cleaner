from engine.csv_parser import load_csv
from engine.issue_detector import detect_missing_values, detect_duplicates
from engine.schema_inference import infer_column_type, infer_schema, dtype_mapping
from engine.cleaner import clean_data

df = load_csv("data/raw/online_retail_real_world.csv")

#if df is not None:
    # print("Missing Values:")
    # print(detect_missing_values(df))

    # print("\nDuplicate order_id values:")
    # print(detect_duplicates(df, "order_id"))

    # print("\nDuplicate customer_id values:")
    # print(detect_duplicates(df, "customer_id"))  

print(df.dtypes)

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
