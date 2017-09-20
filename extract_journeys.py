#!/usr/bin/env python3

import sqlite3
from sqlite3 import Error
import json

conn = sqlite3.connect("activity.sqlite")

cur = conn.cursor()

query = '''
select Latitude,                    --  0
       Longitude,                   --  1
       OriginAimedDepartureTime,    --  2
       OriginRef,                   --  3
       DestinationRef,              --  4
       DirectionRef,                --  5
       OperatorRef,                 --  6
       LineRef,                     --  7
       VehicleRef,                  --  8
       SerialNo,                    --  9
       RecordedAtTime               -- 10
  from activity
  where date(RecordedAtTime) == "2017-04-26" and
        latitude < 52.6 and
        longitude > -0.2
  order by OriginAimedDepartureTime,
           OriginRef,
           DestinationRef,
           DirectionRef,
           OperatorRef,
           LineRef,
           VehicleRef,
           SerialNo
'''

cur.execute(query)

rows = cur.fetchall()

current = '';
result = []
journey = {}
for row in rows:
    this = ' '.join(row[2:9])
    if current != this:
        if journey:
            result.append(journey)
        journey = {}
        journey['name'] = this
        journey['points'] = []
        journey['points_desc'] = []
    current = this
    journey['points'].append(row[0:2])
    journey['points_desc'].append(str(row[9]) + ' ' + row[10])
result.append(journey)

print('var journies =')
print(json.dumps(result, indent=4))
