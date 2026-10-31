-- All rates and mean spending use all assigned customers, including zeros.
SELECT channel, segment, COUNT(*) AS assigned, AVG(conversion) AS conversion, AVG(visit) AS visit, AVG(spend) AS spend FROM customers GROUP BY channel, segment ORDER BY channel, segment;
