from sklearn.preprocessing import StandardScaler
import pandas as pd


def ApplyStandardization(df):
    scale = StandardScaler()
    X = df[df.columns[:-1]]
    scaled_data = scale.fit_transform(X)
    df_scaled = pd.DataFrame(scaled_data, columns=df.columns[:-1])
    df_scaled[df.columns[-1]] = df[df.columns[-1]]
    return df_scaled
