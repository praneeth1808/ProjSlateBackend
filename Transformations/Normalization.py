from sklearn.preprocessing import Normalizer
import pandas as pd


def ApplyNormalization(df):
    scale = Normalizer()
    X = df[df.columns[:-1]]
    scaled_data = scale.fit_transform(X)
    df_scaled = pd.DataFrame(scaled_data, columns=df.columns[:-1])
    df_scaled[df.columns[-1]] = df[df.columns[-1]]
    return df_scaled
