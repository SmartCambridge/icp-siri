-- Extract in-journey reporting frequency from activity reports

\a
\f ,
\o deltas.csv

SELECT 
   delta,
   COUNT(*)
FROM (
    SELECT
      EXTRACT(
        EPOCH FROM recordedattime-LAG(recordedattime) OVER w
      ) as delta
    FROM activity
    WHERE dup = FALSE
    WINDOW w AS (
      PARTITION BY vehiclemonitoringref, originref, originaimeddeparturetime
      ORDER BY recordedattime
    )
) AS foo
GROUP BY
  delta
ORDER BY 
  delta ASC;
