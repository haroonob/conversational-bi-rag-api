## Top 5 products by revenue in UK last month
SELECT Description as product_name, SUM(Quantity * UnitPrice) AS revenue FROM orders WHERE Country = 'United Kingdom' AND InvoiceDate BETWEEN '2025-06-01' AND '2025-06-30' GROUP BY Description ORDER BY revenue DESC LIMIT 5;


## What is the total quantity sold for WHITE HANGING HEART T-LIGHT HOLDER?
SELECT SUM(Quantity) FROM orders WHERE Description = 'WHITE HANGING HEART T-LIGHT HOLDER';

## Show me total revenue by country for July 2024.
SELECT Country, SUM(Quantity * UnitPrice) AS revenue FROM orders WHERE InvoiceDate BETWEEN '2024-07-01' AND '2024-07-31' GROUP BY Country ORDER BY revenue DESC;

## List the top 5 products by quantity sold in the last month.
SELECT Description, SUM(Quantity) AS quantity
FROM orders
WHERE InvoiceDate BETWEEN NOW() - INTERVAL '1 month' AND NOW()
GROUP BY Description
ORDER BY quantity DESC
LIMIT 5;

## What was the average unit price for product code 85123A?
A:SELECT AVG(unitprice) AS avg_unit_price
FROM orders
WHERE stockcode = '85123A';

## Give me the total revenue per customer in the UK.
SELECT   SUM(quantity * unitprice) AS total_revenue
FROM orders
WHERE country = 'United Kingdom'
GROUP BY customerid;