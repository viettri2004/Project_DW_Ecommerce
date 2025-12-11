-- 1. KPI Tổng hợp: Tổng Doanh thu, Tổng Giao dịch, và AOV (Average Order Value)
-----------------------------------------------------------------------------
SELECT
    SUM(fs.totalrevenue) AS "Total Revenue (USD)",
    COUNT(DISTINCT fs.invoiceno) AS "Total Transactions",
    (SUM(fs.totalrevenue) / COUNT(DISTINCT fs.invoiceno)) AS "AOV (USD)"
FROM fact_sales fs;

-- 2. Phân tích Xu hướng: Doanh thu theo Năm/Tháng
--------------------------------------------------
-- Dùng để nhận diện tính mùa vụ và tốc độ tăng trưởng
SELECT
    dd.year,
    dd.month,
    SUM(fs.totalrevenue) AS "Monthly Revenue"
FROM fact_sales fs
JOIN dim_date dd ON fs.date_sk = dd.date_sk
GROUP BY dd.year, dd.month
ORDER BY dd.year, dd.month;

-- 3. Phân tích Địa lý: Top 5 Quốc gia đóng góp Doanh thu
----------------------------------------------------------
-- Dùng để xác định thị trường trọng tâm
WITH TotalRevenue AS (
    SELECT SUM(totalrevenue) AS TotalRev FROM fact_sales
)
SELECT
    dc.country AS "Country",
    SUM(fs.totalrevenue) AS "Revenue by Country",
    (SUM(fs.totalrevenue) * 100.0 / (SELECT TotalRev FROM TotalRevenue)) AS "Revenue Share (%)"
FROM fact_sales fs
JOIN dim_customer dc ON fs.customer_sk = dc.customer_sk
GROUP BY dc.country
ORDER BY "Revenue by Country" DESC
LIMIT 5;

-- 4. Phân tích Sản phẩm: Top 10 Sản phẩm bán chạy nhất theo Doanh thu
--------------------------------------------------------------------
SELECT
    dp.stockcode AS "Stock Code",
    dp.description AS "Product Description",
    SUM(fs.totalrevenue) AS "Total Revenue"
FROM fact_sales fs
JOIN dim_product dp ON fs.product_sk = dp.product_sk
GROUP BY 1, 2
ORDER BY "Total Revenue" DESC
LIMIT 10;