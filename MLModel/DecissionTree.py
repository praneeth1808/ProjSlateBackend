from sklearn.tree import DecisionTreeClassifier
from sklearn.metrics import mean_absolute_error, mean_squared_error
import numpy as np
from sklearn.metrics import accuracy_score
from sklearn.tree import DecisionTreeRegressor


def DecissionTreeClassifierModel(X_train, X_test, y_train, y_test):
    clf = DecisionTreeClassifier()
    clf = clf.fit(X_train, y_train)
    print(y_train)
    print(clf.predict(X_train))
    return {"Model": clf, "Scores":
            {"Train Accuracy": accuracy_score(y_train, clf.predict(X_train)),
             "Test Accuracy": accuracy_score(y_test, clf.predict(X_test))}
            }


def DecissionTreeRegressorModel(X_train, X_test, y_train, y_test):
    clf = DecisionTreeRegressor()
    clf = clf.fit(X_train, y_train)
    y_pred = clf.predict(X_test)
    mae = mean_absolute_error(y_test, y_pred)
    mse = mean_squared_error(y_test, y_pred)
    rmse = np.sqrt(mse)
    return {"Model": clf, "Scores": {"mae": mae, "mse": mse, "rmse": rmse}}


def DecissionTreeModel(X_train, X_test, y_train, y_test):
    try:
        return DecissionTreeClassifierModel(X_train, X_test, y_train, y_test)
    except:
        return DecissionTreeRegressorModel(X_train, X_test, y_train, y_test)
