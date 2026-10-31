-- All rates and mean spending use all assigned customers, including zeros.
SELECT segment, SUM(conversion) AS conversions, COUNT(*) AS assigned, AVG(conversion) AS rate FROM customers GROUP BY segment;
