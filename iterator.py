#!/usr/bin/env python3

# Iteratively query a table of unique journey data grouping by
# all posible combinations of columns to establish which
# combinations are unique

import itertools
import psycopg2

fields = (
    'vehiclemonitoringref',
    'lineref',
    'directionref',
    'datedvehiclejourneyref',
    'operatorref',
    'originref',
    'destinationref',
    'originaimeddeparturetime',
    'date(originaimeddeparturetime)'
    )

conn = psycopg2.connect("dbname='icp' host='localhost'")
cur = conn.cursor()

results = []

# Generate all possible combinations of fields from length 1
# in order by increasing length
for length in range(1, len(fields)+1):
  for subset in itertools.combinations(fields, length):
    list = ', '.join(subset)

    query = "select count(*), " + list + " from journies group by " + list + " having count(*) > 1"
    cur.execute(query)
    rows = cur.fetchall()

    # If there were no rows (i.e. this selection was unique)
    if len(rows) == 0:
        # Ignore ff there are pre-existing shorter matches
        for result in results:
            if set(result).issubset(set(subset)):
                break
        # ...otherwuise remember this
        else:
            results.append(subset)
            print(list)
