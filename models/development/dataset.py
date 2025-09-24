# dataset.py
"""
Sample dataset loader for model training.
"""
import pandas as pd

def load_data(path):
    df = pd.read_csv(path)
    X = df.drop('target', axis=1)
    y = df['target']
    return X, y
