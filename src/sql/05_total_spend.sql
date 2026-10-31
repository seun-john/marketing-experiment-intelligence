-- All rates and mean spending use all assigned customers, including zeros.
SELECT segment, SUM(spend) AS total_spend FROM customers GROUP BY segment;
