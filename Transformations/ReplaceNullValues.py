import pandas as pd
from sklearn.impute import SimpleImputer


def ReplaceNulls(df, cols, option):
    if cols == "All":
        cols = list(df.columns)

    df_copy = df.copy()
    print(cols, option)
    for col in cols:
        df_copy[col] = ReplaceColNulls(df_copy[col], option)
    return df_copy


def ReplaceColNulls(df_col, option):
    if option == "Mean":
        df_col.fillna(round(df_col.mean(), 2), inplace=True)
        return df_col
    elif option == "Median":
        df_col.fillna(round(df_col.median(), 2), inplace=True)
        return df_col
    else:
        df_col.fillna(round(df_col.mode().values[0], 2), inplace=True)
        return df_col
