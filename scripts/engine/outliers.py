

def detect_outliers(df, schema):
    outliers = {}
    for col in df.columns:
        expected_type = schema.get(col)
        # Loop through columns and check for numeric values
        if expected_type == "numeric":
            # define lower and upper using IQR
            Q1 = df[col].quantile(0.25)
            Q3 = df[col].quantile(0.75)
            IQR = Q3 - Q1
            lower = Q1 - 1.5 * IQR
            upper = Q3 + 1.5 * IQR
            # find outliers
            outliers[col] = df[(df[col] < lower) | (df[col] > upper)]
    return outliers

