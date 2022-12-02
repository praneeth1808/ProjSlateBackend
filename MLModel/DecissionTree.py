from sklearn.tree import DecisionTreeClassifier
from sklearn.metrics import mean_absolute_error, mean_squared_error
import numpy as np
from sklearn.metrics import accuracy_score
from sklearn.tree import DecisionTreeRegressor


def DecissionTreeClassifierModel(X_train, X_test, y_train, y_test):
    clf = DecisionTreeClassifier()
    clf = clf.fit(X_train, y_train)
    return {"Model": clf, "Scores":
            {"Training Score": accuracy_score(y_train, clf.predict(X_train)),
             "Testing Score": accuracy_score(y_test, clf.predict(X_test))}
            }


def DecissionTreeRegressorModel(X_train, X_test, y_train, y_test):
    clf = DecisionTreeRegressor()
    clf = clf.fit(X_train, y_train)
    return {"Model": clf, "Scores":
            {"Training Score": accuracy_score(y_train, clf.predict(X_train)),
             "Testing Score": accuracy_score(y_test, clf.predict(X_test))}
            }
