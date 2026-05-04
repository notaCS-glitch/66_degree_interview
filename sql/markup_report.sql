SELECT
    p.branch,
    p.city,
    ROUND(SUM(s.markup_amount), 2) AS total_profit,
    ROUND(AVG(p.markup_rate), 4) AS avg_markup_percentage
FROM sales s

JOIN product_location p
ON s.product_location_id = p.product_location_id

GROUP BY p.branch
ORDER BY total_profit DESC;