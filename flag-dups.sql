-- Set the DUP flag on the second and subsequent records
-- that have identical recordedattime..vehicleref entries

UPDATE
  activity
SET
  dup = TRUE
WHERE
  serialno IN (
    SELECT
      serialno
    FROM (
      SELECT
        serialno,
        Row_Number() OVER (
          PARTITION BY
            recordedattime,
            validuntiltime,
            vehiclemonitoringref,
            lineref, directionref,
            dataframeref,
            datedvehiclejourneyref,
            publishedlinename,
            operatorref,
            vehiclefeatureref,
            originref,
            originname,
            destinationref,
            destinationname,
            originaimeddeparturetime,
            monitored,
            inpanic,
            longitude,
            latitude,
            bearing,
            delay,
            vehicleref
          ORDER BY
            recordedattime,
            validuntiltime,
            vehiclemonitoringref,
            lineref,
            directionref,
            dataframeref,
            datedvehiclejourneyref,
            publishedlinename,
            operatorref,
            vehiclefeatureref,
            originref,
            originname,
            destinationref,
            destinationname,
            originaimeddeparturetime,
            monitored,
            inpanic,
            longitude,
            latitude,
            bearing,
            delay,
            vehicleref
        ) AS rank
      FROM activity
    ) AS a
    WHERE rank > 1
  );