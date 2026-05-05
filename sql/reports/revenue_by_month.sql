SELECT
    strftime('%Y', date) AS year,
    strftime('%m', date) AS month,
    ROUND(SUM(s.total), 2) AS revenue
FROM sales s
GROUP BY year, month;
