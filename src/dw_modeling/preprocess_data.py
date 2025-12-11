import pandas as pd
import numpy as np
import os

current_dir = os.path.dirname(os.path.abspath(__file__))
project_root = os.path.join(current_dir, '..', '..')

RAW_DATA_PATH = os.path.join(project_root, 'data', '01_raw', 'online_retail.csv')
CLEAN_DATA_PATH = os.path.join(project_root, 'data', '02_intermediate', 'clean_transactions.csv')

def preprocess_data(file_path):
    """
    Perform raw data preprocessing steps, including critical fix for floating point precision.
    """
    print(f"Starting to read data from: {file_path}")
    df = pd.read_csv(file_path, encoding='latin-1')

    # Filter negative values for Quantity and UnitPrice
    initial_rows = len(df)
    df_clean = df[(df['Quantity'] > 0) & (df['UnitPrice'] > 0)].copy()
    rows_after_filter = len(df_clean)
    print(f"Removed: {initial_rows - rows_after_filter} invalid rows (returns/cancellations, negative prices).")

    # Handle missing CustomerID
    missing_customer_id = df_clean['CustomerID'].isnull().sum()
    df_clean['CustomerID'] = df_clean['CustomerID'].fillna(99999)
    df_clean['CustomerID'] = df_clean['CustomerID'].astype(int) 
    print(f"Assigned walk-in code (99999) to {missing_customer_id} rows missing CustomerID.")

    # Normalize DateTime
    df_clean['InvoiceDate'] = pd.to_datetime(df_clean['InvoiceDate'])
    print("Normalized InvoiceDate.")
    
    # Floating Point Precision (Khắc phục lỗi sai số tài chính)
    # Lỗi: Tính toán TotalRevenue gặp sai số do số thực (ex: 75.60000000000001)
    # Khắc phục: Làm tròn UnitPrice và TotalRevenue về 2 chữ số thập phân
    df_clean['UnitPrice'] = df_clean['UnitPrice'].round(2)
    df_clean['TotalRevenue'] = (df_clean['Quantity'] * df_clean['UnitPrice']).round(2)
    print("CRITICAL FIX: Applied .round(2) to UnitPrice and TotalRevenue to fix floating point precision errors.")

    # Clean up key Dimension columns (Strip whitespace) For SQL joins
    df_clean['StockCode'] = df_clean['StockCode'].astype(str).str.strip()
    df_clean['Description'] = df_clean['Description'].astype(str).str.strip()
    df_clean['Country'] = df_clean['Country'].astype(str).str.strip()
    print("Cleaned whitespace from key Dimension columns (StockCode, Description, Country).")


    print("\nDataframe info after preprocessing:")
    print(df_clean.info())

    return df_clean

if __name__ == '__main__':
    os.makedirs(os.path.dirname(CLEAN_DATA_PATH), exist_ok=True)

    df_processed = preprocess_data(RAW_DATA_PATH)

    df_processed.to_csv(CLEAN_DATA_PATH, index=False, encoding='utf-8')
    print(f"\nClean data saved at: {CLEAN_DATA_PATH}")