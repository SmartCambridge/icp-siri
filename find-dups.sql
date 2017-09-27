-- Find records containing duplicated recordedattime..vehicleref

SELECT
  COUNT(*)
FROM
  activity
GROUP BY
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
HAVING
  COUNT(*) > 1 ;