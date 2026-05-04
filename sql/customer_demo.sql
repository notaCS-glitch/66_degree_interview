SELECT
    c.customer_type,
    c.gender,
--    p.product_line,
--    p.city,
    COUNT(s.invoice_id) AS number_of_trips,
    ROUND(AVG(s.total), 2) AS avg_spent_per_trip,
    ROUND(AVG(s.rating), 2) AS avg_rating,
    ROUND(SUM(s.total), 2) AS total_revenue
FROM sales s

JOIN customer c
ON s.customer_id = c.customer_id

JOIN product_location p
on s.product_location_id = p.product_location_id

GROUP BY
    c.customer_type
    , c.gender
--    , p.product_line
--    , p.city
ORDER BY total_revenue DESC;