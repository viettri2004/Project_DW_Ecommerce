import pandas as pd
from sqlalchemy import create_engine, text
import os

DB_URL = "postgresql+psycopg2://postgres:130604@127.0.0.1:5432/ecommerce_dw"

current_dir = os.path.dirname(os.path.abspath(__file__))
project_root = os.path.join(current_dir, '..', '..')
CLEAN_DATA_PATH = os.path.join(project_root, 'data', '02_intermediate', 'clean_transactions.csv')

def extract_dim_data(df):
    """Trích xuất dữ liệu Dimension duy nhất và làm sạch bổ sung."""
    df.columns = df.columns.str.lower()
    
    # Dim_Customer
    dim_customer_data = df[['customerid', 'country']].drop_duplicates(subset=['customerid']).copy()

    # Dim_Product
    dim_product_data = df[['stockcode', 'description']].drop_duplicates().copy()
    dim_product_data = dim_product_data[dim_product_data['description'].astype(str).str.strip().str.len() > 1].copy()
    dim_product_data = dim_product_data.drop_duplicates(subset=['stockcode']).copy()

    # Dim_Date
    df['invoicedateonly'] = df['invoicedate'].dt.normalize()
    dim_date_data = df['invoicedateonly'].drop_duplicates().to_frame()
    dim_date_data.columns = ['fulldate']
    dim_date_data['year'] = dim_date_data['fulldate'].dt.year
    dim_date_data['month'] = dim_date_data['fulldate'].dt.month
    dim_date_data['dayofweek'] = dim_date_data['fulldate'].dt.day_name()
    dim_date_data['date_sk'] = dim_date_data['fulldate'].dt.strftime('%Y%m%d').astype(int)

    return dim_customer_data, dim_product_data, dim_date_data

def load_dw(df_transactions, db_engine):
    """Thực hiện ETL: Load Dimension và Fact Tables."""
    print("Starting DW Load...")

    # RESET SCHEMA 
    schema_path = os.path.join(os.path.dirname(__file__), 'create_schema.sql')
    if os.path.exists(schema_path):
        with open(schema_path, 'r', encoding='utf-8') as f:
            schema_sql = f.read()
        statements = [stmt.strip() for stmt in schema_sql.split(';') if stmt.strip()]
        with db_engine.connect() as conn:
            for stmt in statements:
                conn.execute(text(stmt))
            conn.commit()
        print("Schema created/reset.")

    df_transactions.columns = df_transactions.columns.str.lower()
    dim_customer_data, dim_product_data, dim_date_data = extract_dim_data(df_transactions)

    # LOAD DIMENSIONS
    
    # Load dim_date
    dim_date_data[['date_sk', 'fulldate', 'year', 'month', 'dayofweek']].to_sql(
        'dim_date', db_engine, if_exists='append', index=False, chunksize=1000
    )
    print(f"Loaded dim_date: {len(dim_date_data)} rows.")

    # Load dim_product
    dim_product_data[['stockcode', 'description']].to_sql(
        'dim_product', db_engine, if_exists='append', index=False, chunksize=1000
    )
    print(f"Loaded dim_product: {len(dim_product_data)} rows.")

    # Load dim_customer
    dim_customer_data[['customerid', 'country']].to_sql(
        'dim_customer', db_engine, if_exists='append', index=False, chunksize=1000
    )
    print(f"Loaded dim_customer: {len(dim_customer_data)} rows.")
    
    # PREPARE FACT DATA (Mapping SK)
    print("Starting SK mapping...")

    with db_engine.connect() as conn:
        dim_cust_map = pd.read_sql_query('SELECT customer_sk, customerid FROM dim_customer', conn)
        dim_prod_map = pd.read_sql_query('SELECT product_sk, stockcode FROM dim_product', conn)
        dim_date_map = pd.read_sql_query('SELECT date_sk, fulldate FROM dim_date', conn)
        
    dim_date_map['fulldate'] = pd.to_datetime(dim_date_map['fulldate']).dt.normalize()
    df_transactions['fulldate'] = df_transactions['invoicedate'].dt.normalize()

    # Mapping
    df_fact = pd.merge(df_transactions, dim_cust_map, on='customerid', how='left')
    df_fact = pd.merge(df_fact, dim_prod_map, on='stockcode', how='left')
    df_fact = pd.merge(df_fact, dim_date_map, on='fulldate', how='left')
    
    df_fact = df_fact.dropna(subset=['product_sk', 'customer_sk', 'date_sk'])

    # LOAD FACT TABLE
    fact_cols = ['invoiceno', 'quantity', 'unitprice', 'totalrevenue', 'date_sk', 'product_sk', 'customer_sk']

    df_fact[fact_cols].to_sql(
        'fact_sales', db_engine, if_exists='append', index=False, method='multi', chunksize=1000
    )
    print(f"Loaded fact_sales with {len(df_fact)} rows.")
    print("\nETL process completed successfully!")

if __name__ == '__main__':
    try:
        engine = create_engine(DB_URL)
        df_clean = pd.read_csv(CLEAN_DATA_PATH) 
        df_clean['InvoiceDate'] = pd.to_datetime(df_clean['InvoiceDate'])
        load_dw(df_clean, engine)
    except Exception as e:
        print(f"Error in ETL process: {e}")
        print("Please check the DB_URL and database status.")