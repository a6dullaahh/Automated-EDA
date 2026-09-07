import pandas as pd


def loader(file):
    """Load a CSV or Excel file (path or file-like object) into a DataFrame."""
    name = getattr(file, "name", str(file))
    if name.lower().endswith((".xlsx", ".xls")):
        return pd.read_excel(file)
    return pd.read_csv(file)
