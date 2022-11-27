from sklearn.linear_model import LinearRegression, LogisticRegression
from sklearn.metrics import mean_absolute_error, mean_squared_error
import numpy as np


def LinearRegressionModel(X_train, X_test, y_train, y_test):
    lr = LinearRegression()
    lr = lr.fit(X_train, y_train)
    y_pred = lr.predict(X_test)
    mae = mean_absolute_error(y_test, y_pred)
    mse = mean_squared_error(y_test, y_pred)
    rmse = np.sqrt(mse)
    Training_Score = lr.score(X_train, y_train)
    Testing_score = lr.score(X_test, y_test)
    return {"Model": lr, "Scores": {"Training Score": Training_Score, "Testing Score": Testing_score}}


def LinearClassificationModel(X_train, X_test, y_train, y_test):
    print("Got to Classification")
    lr = LogisticRegression()
    lr = lr.fit(X_train, y_train)
    Training_Score = lr.score(X_train, y_train)
    Testing_score = lr.score(X_test, y_test)
    return {"Model": lr, "Scores": {"Training Score": Training_Score, "Testing Score": Testing_score}}
