# sample_mlflow_register.py
"""
Sample code for registering a model with MLflow Model Registry.
"""
import mlflow
import mlflow.sklearn
from sklearn.ensemble import RandomForestClassifier
from sklearn.datasets import load_iris

# Train a sample model
X, y = load_iris(return_X_y=True)
model = RandomForestClassifier().fit(X, y)

# Log and register the model
with mlflow.start_run():
    mlflow.sklearn.log_model(model, "model", registered_model_name="IrisRFModel")
    mlflow.log_metric("accuracy", model.score(X, y))
