-- All rates and mean spending use all assigned customers, including zeros.
SELECT history_segment, segment, COUNT(*) AS assigned, AVG(conversion) AS conversion, AVG(visit) AS visit, AVG(spend) AS spend FROM customers GROUP BY history_segment, segment ORDER BY history_segment, segment;
