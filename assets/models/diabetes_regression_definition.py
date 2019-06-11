from sklearn import datasets, linear_model
from sklearn.metrics import mean_squared_error, r2_score
from joblib import dump
import pandas as pd

diabetes_train = pd.read_csv('diabetes_train.csv', index_col=None)
diabetes_X_train = diabetes_train.iloc[:, 0:-1]
diabetes_y_train = diabetes_train[['y']]
diabetes_test = pd.read_csv('diabetes_feedback.csv', index_col=None)
diabetes_X_test = diabetes_test.iloc[:, 0:-1]
diabetes_y_test = diabetes_test[['y']]

model = linear_model.LinearRegression()
model.fit(diabetes_X_train, diabetes_y_train)

print("R-squared on train set: {:.2f}".format(r2_score(diabetes_y_train, model.predict(diabetes_X_train))))
print("R-squared on test set: {:.2f}".format(r2_score(diabetes_y_test, model.predict(diabetes_X_test))))

model_path="diabetes_regression.joblib"
dump(model, model_path)

print("Model has been stored to file: {}".format(model_path))
