# model.py
"""
Sample model class for training.
"""
from sklearn.linear_model import LogisticRegression

class MyModel:
    def __init__(self, **kwargs):
        self.model = LogisticRegression(**kwargs)
    def fit(self, X, y):
        self.model.fit(X, y)
    def predict(self, X):
        return self.model.predict(X)
