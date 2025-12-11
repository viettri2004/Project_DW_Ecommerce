# E-commerce Data Warehouse & Market Basket Analysis

This project implements a Data Warehouse (DW) for E-commerce data and applies Market Basket Analysis (MBA) using the Online Retail Dataset. The project includes data preprocessing, data warehouse modeling, ETL processes, and association rule mining.

## Project Overview

This e-commerce analytics project focuses on:
- **Data Warehousing**: Building a star schema data warehouse from transactional data
- **ETL Processes**: Extracting, transforming, and loading data into the warehouse
- **Market Basket Analysis**: Discovering association rules between products using the Apriori algorithm
- **Business Intelligence**: Analyzing customer purchasing patterns and product relationships

## Project Structure

```
Project_DW_Ecommerce/
├── data/
│   ├── 01_raw/
│   │   └── online_retail.csv              # Raw Online Retail dataset
│   └── 02_intermediate/
│       └── clean_transactions.csv         # Cleaned and preprocessed data
├── src/
│   ├── dw_modeling/
│   │   ├── create_schema.sql              # Data warehouse schema creation
│   │   ├── etl_load.py                    # ETL pipeline for data warehouse
│   │   └── preprocess_data.py             # Data preprocessing script
│   ├── data_analysis/
│   │   └── 01_olap_queries.sql            # OLAP analytical queries
│   └── ml_model/
│       ├── market_basket_analysis.py      # Apriori algorithm implementation
│       ├── rule_analysis.py               # Association rules analysis
│       └── output_rules.csv               # Generated association rules
├── venv_ecommerce_dw/                     # Python virtual environment
├── ecommerce_dw.db                        # SQLite database (if used)
├── requirements.txt                       # Python dependencies
└── README.md                              # This file
```

## Technology Stack

- **Programming Language**: Python 3.x
- **Data Processing**: Pandas, NumPy
- **Database**: PostgreSQL
- **ML Libraries**: mlxtend (for Apriori algorithm)
- **Data Analysis**: SQL for OLAP queries

## Quick Start

### 1. Environment Setup
```bash
# Create and activate virtual environment
python -m venv venv_ecommerce_dw
.\venv_ecommerce_dw\Scripts\activate  # Windows
# source venv_ecommerce_dw/bin/activate  # macOS/Linux

# Install dependencies
pip install -r requirements.txt
```

### 2. Data Preprocessing
```bash
python src/dw_modeling/preprocess_data.py
```
This cleans the raw data and creates intermediate processed data.

### 3. Data Warehouse Creation
```bash
# Create database schema
python src/dw_modeling/create_schema.sql  

# Load data into warehouse
python src/dw_modeling/etl_load.py
```

### 4. Market Basket Analysis
```bash
# Generate association rules
python src/ml_model/market_basket_analysis.py

# Analyze the rules
python src/ml_model/rule_analysis.py
```

## Key Features

### Data Warehouse Design
- **Star Schema**: Fact table with dimension tables for customers, products, time, and geography
- **ETL Pipeline**: Automated data transformation and loading processes
- **Data Quality**: Comprehensive data cleaning and validation

### Market Basket Analysis
- **Apriori Algorithm**: Discover frequent itemsets and association rules
- **Rule Analysis**: Analyze rules by support, confidence, and lift metrics
- **Business Insights**: Identify product relationships and cross-selling opportunities

### Analytical Capabilities
- **OLAP Queries**: Multi-dimensional data analysis
- **Customer Segmentation**: RFM analysis (ready for implementation)
- **Product Analysis**: Sales patterns and trend identification

## Sample Analysis Results

Based on the current dataset analysis:

### Association Rules Summary
- **Total Rules Generated**: 351 association rules
- **High Lift Rules (Lift > 20)**: 12 rules (3.4%)
- **Medium Lift Rules (10-20)**: 149 rules (42.4%)
- **Low Lift Rules (< 10)**: 190 rules (54.1%)

### Example Product Association
- **Product Pair**: JUMBO SHOPPER VINTAGE RED PAISLEY → JUMBO BAG RED RETROSPOT
- **Support**: 3.41% (appears in 3.41% of transactions)
- **Lift**: 5.53 (products are 5.53 times more likely to be bought together than randomly)

## Data Sources

- **Primary Dataset**: Online Retail Dataset
- **Source**: UCI Machine Learning Repository
- **Description**: Transaction data from a UK-based online retailer
- **Time Period**: 2010-2011
- **Records**: ~500,000+ transactions