import pandas as pd


def get_shape(df):
    return df.shape


def get_dtypes(df):
    return df.dtypes.astype(str).to_frame("dtype")


def get_missing(df):
    missing = df.isnull().sum()
    pct = (missing / len(df) * 100).round(2)
    out = pd.DataFrame({"missing_count": missing, "missing_pct": pct})
    return out.sort_values("missing_count", ascending=False)


def get_summary(df):
    return df.describe(include="all").transpose()


def get_duplicates(df):
    return df.duplicated().sum()


def get_unique_counts(df):
    return df.nunique().to_frame("unique_values").sort_values("unique_values")


def get_column_types(df):
    numeric = df.select_dtypes(include="number").columns.tolist()
    categorical = df.select_dtypes(include=["object", "category", "bool"]).columns.tolist()
    datetime_cols = df.select_dtypes(include="datetime").columns.tolist()
    return numeric, categorical, datetime_cols
