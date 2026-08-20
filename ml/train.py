from sklearn.model_selection import train_test_split
from sklearn.datasets import load_iris
from sklearn.linear_model import LogisticRegression
from sklearn.metrics import accuracy_score

import joblib

iris = load_iris()

X = iris.data
y = iris.target

X_train, X_test, y_train, y_test = train_test_split(
    X,
    y,
    test_size=0.2,
    random_state=42
)

model = LogisticRegression()

model.fit(X_train, y_train)

y_pred = model.predict(X_test)

accuracy = accuracy_score(y_test, y_pred)

print("Accuracy:", accuracy)
joblib.dump(model, "ml/saved_model/iris_model.pkl")
loaded_model = joblib.load("ml/saved_model/iris_model.pkl")

sample = [[5.1, 3.5, 1.4, 0.2]]

prediction = loaded_model.predict(sample)

print("Prediction:", prediction)