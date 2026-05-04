SELECT
    c.gender,
    p.product_line,
    ROUND(SUM(s.total), 2) AS line_revenue,
    ROUND(
        (SUM(s.total) * 100.0) / SUM(SUM(s.total)) OVER(),
        2
    ) AS percent_of_total
FROM sales s

JOIN customer c
ON s.customer_id = c.customer_id

JOIN product_location p
ON s.product_location_id = p.product_location_id

--WHERE c.gender = 'Female'
--WHERE c.gender = 'Male'

GROUP BY c.gender, p.product_line
ORDER BY line_revenue DESC;