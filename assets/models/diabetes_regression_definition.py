from sklearn import datasets, linear_model
from sklearn.metrics import mean_squared_error, r2_score
from joblib import dump

diabetes_data = datasets.load_diabetes()
diabetes_X = diabetes_data.data
diabetes_y = diabetes_data.target

diabetes_X_train = diabetes_X[:-20]
diabetes_y_train = diabetes_y[:-20]
diabetes_X_test = diabetes_X[-20:]
diabetes_y_test = diabetes_y[-20:]

model = linear_model.LinearRegression()
model.fit(diabetes_X_train, diabetes_y_train)

print("R-squared on train set: {:.2f}".format(r2_score(diabetes_y_train, model.predict(diabetes_X_train))))
print("R-squared on test set: {:.2f}".format(r2_score(diabetes_y_test, model.predict(diabetes_X_test))))


model_path="diabetes_regression.joblib"
dump(model, model_path)
