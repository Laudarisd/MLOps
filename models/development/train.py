# train.py
"""
Sample training script for model development.
"""
import pandas as pd
from model import MyModel
from dataset import load_data
import yaml

def main():
    # Load config
    with open('config.yaml', 'r') as f:
        config = yaml.safe_load(f)
    # Load data
    X_train, y_train = load_data(config['data_path'])
    # Initialize and train model
    model = MyModel(**config['model_params'])
    model.fit(X_train, y_train)
    print("Training complete.")

if __name__ == "__main__":
    main()
