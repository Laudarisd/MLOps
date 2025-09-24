import pandas as pd
import os

RAW_DATA_PATH = "../data/raw/data.csv"
PROCESSED_DATA_PATH = "../data/processed/processed_data.csv"
PREPROCESSED_DATA_PATH = "../data/processed/preprocessed_data.csv"

def load_processed_data(path):
    """Load processed data from CSV file."""
    if not os.path.exists(path):
        raise FileNotFoundError(f"Processed data file not found at {path}")
    return pd.read_csv(path)

def preprocess_data(df):
    """Perform data preprocessing steps."""
    # Example: normalize numeric columns
    numeric_cols = df.select_dtypes(include=['float64', 'int64']).columns
    df[numeric_cols] = (df[numeric_cols] - df[numeric_cols].mean()) / df[numeric_cols].std()
    # Add more preprocessing steps as needed
    return df

def save_preprocessed_data(df, path):
    """Save preprocessed data to CSV."""
    os.makedirs(os.path.dirname(path), exist_ok=True)
    df.to_csv(path, index=False)

def main():
    print("Starting data preprocessing...")
    df_processed = load_processed_data(PROCESSED_DATA_PATH)
    print(f"Loaded processed data shape: {df_processed.shape}")
    df_preprocessed = preprocess_data(df_processed)
    print(f"Preprocessed data shape: {df_preprocessed.shape}")
    save_preprocessed_data(df_preprocessed, PREPROCESSED_DATA_PATH)
    print(f"Preprocessed data saved to {PREPROCESSED_DATA_PATH}")

if __name__ == "__main__":
    main()
