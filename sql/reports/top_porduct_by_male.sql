SELECT
    c.gender,
    p.product_line,
    ROUND(SUM(s.total), 2) AS revenue,
    RANK() OVER (ORDER BY SUM(s.total) DESC) AS rank
FROM sales s

JOIN customer c
ON s.customer_id = c.customer_id

JOIN product_location p
ON s.product_location_id = p.product_location_id

WHERE c.gender = 'Male'

GROUP BY c.gender, p.product_line
ORDER BY revenue DESC;