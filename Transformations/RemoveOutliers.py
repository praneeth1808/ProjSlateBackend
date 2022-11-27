import pandas as pd
import numpy as np
import scipy.stats as stats


def removeOutliers(df, method):
    if method == "IQR":
        return removeOutliers_IQR(df)
    else:
        return removeOutliers_ZScore(df)


def removeOutliers_IQR(df):
    df_copy = df.copy()
    df_copy = df_copy.dropna(axis=0)
    for i in df_copy.columns:
        df_copy = removeOutliers_IQR_col(df_copy, i)
    return df_copy


def removeOutliers_IQR_col(df, col):
    df_copy = df.copy()
    Q3 = np.quantile(df_copy[col], 0.75)
    Q1 = np.quantile(df_copy[col], 0.25)
    IQR = Q3 - Q1
    lower_range = Q1 - 1.5 * IQR
    upper_range = Q3 + 1.5 * IQR
    outlier_free_list = [x for x in df_copy[col]
                         if ((x > lower_range) & (x < upper_range))]
    return df_copy.loc[df_copy[col].isin(outlier_free_list)]


def removeOutliers_ZScore(df):
    df_copy = df.copy()
    df_copy = df_copy.dropna(axis=0)
    for i in df_copy.columns:
        df_copy = removeOutliers_ZScore_col(df_copy, i)
    return df_copy


def removeOutliers_ZScore_col(df, col):
    df_copy = df.copy()
    upperLimit = df_copy[col].mean() + 3*df_copy[col].std()
    lowerLimit = df_copy[col].mean() - 3*df_copy[col].std()
    return df_copy[(df_copy[col] < upperLimit) & (df_copy[col] > lowerLimit)]
