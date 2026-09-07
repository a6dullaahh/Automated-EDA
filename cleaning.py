import pandas as pd


def drop_duplicates(df):
    return df.drop_duplicates().reset_index(drop=True)


def handle_missing(df, strategy="drop", fill_value=None):
    if strategy == "drop":
        return df.dropna().reset_index(drop=True)
    if strategy == "mean":
        return df.fillna(df.mean(numeric_only=True))
    if strategy == "median":
        return df.fillna(df.median(numeric_only=True))
    if strategy == "mode":
        return df.fillna(df.mode().iloc[0])
    if strategy == "constant":
        return df.fillna(fill_value)
    return df


def convert_dtype(df, column, dtype):
    df = df.copy()
    try:
        df[column] = df[column].astype(dtype)
    except (ValueError, TypeError):
        pass
    return df


def detect_outliers_iqr(df, column):
    q1 = df[column].quantile(0.25)
    q3 = df[column].quantile(0.75)
    iqr = q3 - q1
    lower, upper = q1 - 1.5 * iqr, q3 + 1.5 * iqr
    return df[(df[column] < lower) | (df[column] > upper)]


def remove_outliers_iqr(df, column):
    outliers = detect_outliers_iqr(df, column)
    return df.drop(outliers.index).reset_index(drop=True)


def strip_whitespace(df):
    df = df.copy()
    for col in df.select_dtypes(include="object").columns:
        df[col] = df[col].astype(str).str.strip()
    return df
