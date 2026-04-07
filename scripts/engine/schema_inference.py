import pandas as pd

# This module is responsible for outlining the datatypes by matching column names to expected datatypes.

# Dictionary to map column name patterns to expected datatypes
inference_rules = {
    "datetime": ["date", "time", "timestamp", "datetime", "created", "updated", "modified", "dob", "birthdate"
     ],
    "id": ["id", "_id", "user_id", "customer_id", "order_id", "product_id", "transaction_id", "account_id", "code", "sku", "reference"
    ],
    "numeric": ["price", "amount", "quantity", "total", "cost", "count", "weight", "score", "rating", "age", "subtotal", "discount", "qty", "age", "rate", "balance", "expense"
    ],
	"boolean": ["is_", "has_", "can_", "should_", "enable_", "active", "flag", "valid", "deleted", "verified"
    ],
    "string": ["name", "description", "address", "email", "phone", "city", "state", "country", "zip", "postal_code", "email", "type", "brand", "model", "color", "size", "comment", "note"
    ]
}

# This function takes a column name, checks it against the inference rules and returns the inferred datatype.

def infer_column_type(column_name):
    column_name = column_name.lower().strip()  # Normalize to lowercase for matching
    column_tokens = column_name.split("_")  # Split column name into tokens for better matching
   

    priority_order = ["datetime", "id", "numeric", "boolean", "string"]

    for dtype in priority_order:
        keywords = inference_rules[dtype]
        for keyword in keywords:
            if keyword == column_name:
                return dtype
            if "_" not in keyword and keyword in column_tokens:
                return dtype
    return "string"  # Default to string if no patterns match

def infer_schema(df):
    schema = {}# create an empty dict 
    for column in df.columns:
        inferred_type = infer_column_type(column)
        schema[column] = inferred_type
    return schema

# Compare inferred type to pandas dtype create a dict of mismatches
def dtype_mapping(df, schema):
    mismatches = {}
    mapping = {
        "int64": "numeric",
        "float64": "numeric",
        "int32": "numeric",
        "float32": "numeric",
        "object": "string",
        "bool": "boolean",
        "datetime64[ns]": "datetime",
        "str": "string",
    }
    for col in df.columns:
        expected = schema[col]
        actual_dtype = str(df[col].dtype)
        mapped_actual = mapping.get(actual_dtype, "string")  # Default to string if dtype not in mapping
        if expected == 'id':
            if mapped_actual != 'numeric' and mapped_actual != 'string':
                mismatches[col] = {
                 "expected": expected,
                 "actual": mapped_actual
             }
        elif expected != mapped_actual:
             mismatches[col] = {
                "expected": expected,
                 "actual": mapped_actual
             }
    return mismatches 
