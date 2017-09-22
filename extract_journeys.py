#!/usr/bin/env python3

import sqlite3
from sqlite3 import Error
import json

conn = sqlite3.connect("activity.sqlite")

cur = conn.cursor()

query = '''
select at.Latitude,                    --  0
       at.Longitude,                   --  1
       at.OriginAimedDepartureTime,    --  2
       at.OriginRef,                   --  3
       at.DestinationRef,              --  4
       at.DirectionRef,                --  5
       at.OperatorRef,                 --  6
       at.LineRef,                     --  7
       at.VehicleRef,                  --  8
       at.SerialNo,                    --  9
       at.RecordedAtTime,              -- 10
       start.CommonName,               -- 11
       start.LocalityName,             -- 12
       start.Latitude,                 -- 13
       start.Longitude,                -- 14
       end.CommonName,                 -- 15
       end.LocalityName,               -- 16
       end.Latitude,                   -- 17
       end.Longitude                   -- 18
  from activity as at
  left join naptan as start on at.OriginRef = start.ATCOCode
  left join naptan as end on at.DestinationRef = end.ATCOCode
  where date(at.RecordedAtTime) == "2017-08-30" and
        at.latitude < 52.4 and
        at.longitude > -0.2
  order by at.OriginAimedDepartureTime,
           at.OriginRef,
           at.DestinationRef,
           at.DirectionRef,
           at.OperatorRef,
           at.LineRef,
           at.VehicleRef,
           at.SerialNo
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
        journey['name'] = ' '.join((row[2], row[3], row[12], row[11], row[4], row[16], row[15]) + (row[5:9]))
        journey['points'] = []
        journey['points_desc'] = []
        journey['start'] = [row[13], row[14]]
        journey['start_label'] = ', '.join((row[12], row[11]))
        journey['end'] = [row[17], row[18]]
        journey['end_label'] = ', '.join((row[16], row[15]))
    current = this
    journey['points'].append(row[0:2])
    journey['points_desc'].append(str(row[9]) + ' ' + row[10])
result.append(journey)

print('var journies =')
print(json.dumps(result, indent=4))
