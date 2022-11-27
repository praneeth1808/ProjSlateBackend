from sklearn.preprocessing import StandardScaler
import pandas as pd


def ApplyRemoveNullRows(df, cols):
    if cols == "All":
        return df.dropna(axis=0)
    elif len(cols):
        return df.dropna(subset=cols)
    return df.dropna(axis=0)


def ApplyRemoveNullColumns(df, cols):
    return df.dropna(axis=1)
