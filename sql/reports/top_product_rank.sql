SELECT
  p.product_line,
  SUM(total) AS total_sales,
  RANK() OVER (ORDER BY SUM(total) DESC) AS rank
FROM sales s

JOIN product_location p
ON s.product_location_id = p.product_location_id

GROUP BY product_line;