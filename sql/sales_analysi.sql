-- 1. Sales & Profit by Region
SELECT
    region,
    ROUND(SUM(sales), 2) AS total_sales,
    ROUND(SUM(profit), 2) AS total_profit
FROM superstore
GROUP BY region
ORDER BY total_sales DESC;

-- 2. Category-wise Sales & Profit
SELECT
    category,
    ROUND(SUM(sales), 2) AS total_sales,
    ROUND(SUM(profit), 2) AS total_profit
FROM superstore
GROUP BY category;

-- 3. Monthly Sales Trend
SELECT
    DATE_TRUNC('month', order_date) AS month,
    ROUND(SUM(sales), 2) AS monthly_sales
FROM superstore
GROUP BY month
ORDER BY month;

-- 4. Profit Margin by Region
SELECT
    region,
    ROUND(SUM(profit) / SUM(sales) * 100, 2) AS profit_margin
FROM superstore
GROUP BY region;

-- 5. Top 10 Loss-Making Products
SELECT
    product_name,
    ROUND(SUM(profit), 2) AS total_profit
FROM superstore
GROUP BY product_name
HAVING SUM(profit) < 0
ORDER BY total_profit
LIMIT 10;
