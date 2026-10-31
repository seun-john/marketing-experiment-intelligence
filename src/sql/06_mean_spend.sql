-- All rates and mean spending use all assigned customers, including zeros.
SELECT segment, COUNT(*) AS assigned, AVG(spend) AS mean_spend, STDDEV_SAMP(spend) AS sd FROM customers GROUP BY segment;
