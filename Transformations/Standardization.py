from sklearn.preprocessing import StandardScaler
import pandas as pd


def ApplyStandardization(df, cols):
    scale = StandardScaler()
    print(cols == "All")
    if cols == "All":
        X = df[df.columns[:-1]]
        scaled_data = scale.fit_transform(X)
        df_scaled = pd.DataFrame(scaled_data, columns=df.columns[:-1])
        df_scaled[df.columns[-1]] = df[df.columns[-1]]
        return df_scaled
    else:
        X = df[cols]
        scaled_data = scale.fit_transform(X)
        df_scaled = pd.DataFrame(scaled_data, columns=cols)
        df_copy = df.copy()
        for col in cols:
            df_copy[col] = df_scaled[col]
        return df_copy
