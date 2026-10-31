-- All rates and mean spending use all assigned customers, including zeros.
SELECT segment, SUM(visit) AS visits, COUNT(*) AS assigned, AVG(visit) AS rate FROM customers GROUP BY segment;
