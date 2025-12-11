-- PostgreSQL schema for E-commerce DW
-- Drop tables in reverse dependency order (RESET Schema)
DROP TABLE IF EXISTS fact_sales;
DROP TABLE IF EXISTS dim_customer;
DROP TABLE IF EXISTS dim_product;
DROP TABLE IF EXISTS dim_date;

-- 1. Create Dimension Customer
CREATE TABLE dim_customer (
    customer_sk SERIAL PRIMARY KEY, 
    "customerid" INTEGER NOT NULL UNIQUE, 
    country VARCHAR(100)
);

-- 2. Create Dimension Product
CREATE TABLE dim_product (
    product_sk SERIAL PRIMARY KEY, 
    "stockcode" VARCHAR(20) NOT NULL UNIQUE, 
    description VARCHAR(255)
);

-- 3. Create Dimension Date
CREATE TABLE dim_date (
    date_sk INTEGER PRIMARY KEY, 
    fulldate DATE NOT NULL UNIQUE, 
    year INTEGER,
    month INTEGER,
    dayofweek VARCHAR(20)
);

-- 4. Create Fact Sales
CREATE TABLE fact_sales (
    "invoiceno" VARCHAR(20) NOT NULL,
    quantity INTEGER NOT NULL,
    unitprice DECIMAL(10, 4) NOT NULL,
    totalrevenue DECIMAL(10, 4) NOT NULL,

    -- Foreign keys 
    date_sk INTEGER NOT NULL,
    product_sk INTEGER NOT NULL,
    customer_sk INTEGER NOT NULL,

    -- Foreign key constraints
    FOREIGN KEY (date_sk) REFERENCES dim_date(date_sk),
    FOREIGN KEY (product_sk) REFERENCES dim_product(product_sk),
    FOREIGN KEY (customer_sk) REFERENCES dim_customer(customer_sk)
);