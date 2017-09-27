#!/usr/bin/env python3

import sqlite3
#from sqlite3 import Error
#import psycopg2
import json

conn = sqlite3.connect("activity.sqlite")
#conn = psycopg2.connect("dbname='icp' host='localhost'")

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
       at.VehicleRef ,                  --  8
       at.SerialNo,                    --  9
       at.RecordedAtTime,              -- 10
       s.CommonName,               -- 11
       s.LocalityName,             -- 12
       s.Latitude,                 -- 13
       s.Longitude,                -- 14
       e.CommonName,                 -- 15
       e.LocalityName,               -- 16
       e.Latitude,                   -- 17
       e.Longitude                   -- 18
  from activity as at
  left join naptan as s on at.OriginRef = s.ATCOCode
  left join naptan as e on at.DestinationRef = e.ATCOCode
  where at.VehicleRef = 'SCCM-21224' and
        date(at.OriginAimedDepartureTime) = '2017-09-04'
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
