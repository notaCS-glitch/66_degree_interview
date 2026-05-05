SELECT
    p.city,
    p.product_line,
    ROUND(SUM(s.total), 2) AS total_revenue,
    COUNT(s.invoice_id) AS transaction_count

FROM sales s

JOIN product_location p
ON s.product_location_id = p.product_location_id

GROUP BY p.city, p.product_line
ORDER BY total_revenue DESC;