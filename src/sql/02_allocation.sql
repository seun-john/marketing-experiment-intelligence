-- All rates and mean spending use all assigned customers, including zeros.
SELECT segment, COUNT(*) AS customers, COUNT(*)*1.0/(SELECT COUNT(*) FROM customers) AS proportion FROM customers GROUP BY segment;
