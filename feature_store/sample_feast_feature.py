# sample_feast_feature.py
"""
Sample code for defining and ingesting features using Feast (feature store).
"""
from feast import FeatureStore, Entity, FeatureView, Field
from feast.types import Int64, Float32
import pandas as pd

# Define an entity
customer = Entity(name="customer_id", join_keys=["customer_id"])

# Define a feature view
customer_features = FeatureView(
    name="customer_features",
    entities=[customer],
    schema=[
        Field(name="age", dtype=Int64),
        Field(name="income", dtype=Float32),
    ],
    online=True,
)

# Ingest sample data
if __name__ == "__main__":
    store = FeatureStore(repo_path=".")
    df = pd.DataFrame({"customer_id": [1, 2], "age": [30, 40], "income": [50000.0, 60000.0]})
    store.apply([customer, customer_features])
    store.ingest(customer_features, df)
