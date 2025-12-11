# E-commerce Data Warehouse & Market Basket Analysis

This project implements a Data Warehouse (DW) for E-commerce data and applies Market Basket Analysis (MBA) using the Online Retail Dataset.

## Project Structure

```
Project_DW_Ecommerce/
├── data/
│   ├── 01_raw/
│   │   └── online_retail.csv              # Raw data source
│   ├── 02_intermediate/
│   │   └── clean_transactions.csv         # Cleaned data (output from preprocessing)
│   └── 03_dimensions/
│       ├── dim_customer.csv               # Dimension Customer output
│       └── dim_product.csv                # Dimension Product output
├── src/
│   ├── dw_modeling/
│   │   ├── create_schema.sql              # SQL script to create DW tables
│   │   └── etl_transform.py               # ETL script for transforming and loading data
│   ├── data_analysis/
│   │   ├── 01_olap_queries.sql            # OLAP queries
│   │   ├── 02_rfm_segmentation.py         # RFM segmentation
│   │   └── 03_mba_prepare.py              # MBA preparation
│   └── ml_model/
│       ├── market_basket_analysis.py      # Apriori algorithm
│       └── output_rules.csv               # Output association rules
├── reports/
│   ├── final_report.pdf                   # Final report
│   ├── dashboards/
│   │   ├── powerbi_report.pbix            # Power BI dashboard
│   └── analysis_notebooks/
│       └── initial_data_cleaning.ipynb    # Jupyter notebook for initial cleaning
├── requirements.txt                       # Python dependencies
└── README.md                              # This file
```

## Setup Instructions

1. Ensure Python 3.x is installed.
2. Create a virtual environment: `python -m venv venv_ecommerce_dw`
3. Activate the virtual environment:
   - Windows: `.\venv_ecommerce_dw\Scripts\activate`
   - macOS/Linux: `source venv_ecommerce_dw/bin/activate`
4. Install dependencies: `pip install -r requirements.txt`
5. Run preprocessing: `python src/dw_modeling/preprocess_data.py`
6. For DW loading, set up a database (PostgreSQL/SQL Server) and update DB_URL in etl_load.py, then run `python src/dw_modeling/etl_load.py`

## Project Phases

- **Phase I**: Data Preprocessing & DW Building
  - 1.1: Clean raw data
  - 1.2: Design Star Schema
  - 1.3: ETL Load DW

- **Phase II**: OLAP & MBA
  - 2.1: Visualization & OLAP
  - 2.2: Market Basket Analysis

- **Phase III**: Analysis & Discussion

- **Phase IV**: Constraints & Future Development