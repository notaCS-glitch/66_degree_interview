SELECT *
FROM sales s
JOIN customer c ON s.customer_id = c.customer_id
JOIN product_location p ON s.product_location_id = p.product_location_id;