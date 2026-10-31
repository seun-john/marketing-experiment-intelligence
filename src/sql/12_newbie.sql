-- All rates and mean spending use all assigned customers, including zeros.
SELECT newbie, segment, COUNT(*) AS assigned, AVG(conversion) AS conversion, AVG(visit) AS visit, AVG(spend) AS spend FROM customers GROUP BY newbie, segment ORDER BY newbie, segment;
