-- All rates and mean spending use all assigned customers, including zeros.
SELECT segment, COUNT(*) AS customers FROM customers GROUP BY segment;
