import os
import pandas as pd

RAW_DATA_PATH = "../data/raw/data.csv"
PROCESSED_DATA_PATH = "../data/processed/processed_data.csv"

def read_raw_data(path):
    """Read raw data from CSV file."""
    if not os.path.exists(path):
        raise FileNotFoundError(f"Raw data file not found at {path}")
    return pd.read_csv(path)

def clean_data(df):
    """Perform basic data cleaning."""
    # Example: drop rows with missing values
    df_clean = df.dropna()
    # Add more cleaning steps as needed
    return df_clean

def save_processed_data(df, path):
    """Save processed data to CSV."""
    os.makedirs(os.path.dirname(path), exist_ok=True)
    df.to_csv(path, index=False)

def main():
    print("Starting data ingestion...")
    df_raw = read_raw_data(RAW_DATA_PATH)
    print(f"Raw data shape: {df_raw.shape}")
    df_clean = clean_data(df_raw)
    print(f"Processed data shape: {df_clean.shape}")
    save_processed_data(df_clean, PROCESSED_DATA_PATH)
    print(f"Processed data saved to {PROCESSED_DATA_PATH}")

if __name__ == "__main__":
    main()