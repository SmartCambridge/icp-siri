#!/usr/bin/env python3

import arrow
import collections
import xml.etree.ElementTree as ET
import os
import sys
import pandas

service_delivery_counts = collections.Counter()
vehicle_monitoring_counts = collections.Counter()
vehicle_activity_counts = collections.Counter()

file_activities_count = collections.Counter()

vehicle_activity_deltas = []
file_activities = []

base = sys.argv[1]

for file in os.listdir(os.fsencode(base)):
    filename = os.path.join(base, os.fsdecode(file))
    if not filename.endswith(".xml"):
        continue

    # Reciept timestamp, from filename
    basename = os.path.basename(filename)
    timestamp = basename[:10]
    our_timestamp = arrow.get(timestamp)

    tree = ET.parse(filename)
    root=tree.getroot()

    # Service Delivery -> Response Timestamp
    # Siri -> ServiceDelivery -> ResponseTimestamp
    service_delivery = root.find('{http://www.siri.org.uk/siri}ServiceDelivery')
    element = service_delivery.find('{http://www.siri.org.uk/siri}ResponseTimestamp')
    timestamp = element.text
    service_delivery_timestamp = arrow.get(timestamp)
    delta = (our_timestamp - service_delivery_timestamp).total_seconds()
    service_delivery_counts[delta] += 1

    # Vehicle Monitoring Delivery -> Response Timestamp
    vehicle_monitoring_delivery = service_delivery.find('{http://www.siri.org.uk/siri}VehicleMonitoringDelivery')
    element = vehicle_monitoring_delivery.find('{http://www.siri.org.uk/siri}ResponseTimestamp')
    timestamp = element.text
    vehicle_monitoring_timestamp = arrow.get(timestamp)
    delta = (service_delivery_timestamp - vehicle_monitoring_timestamp).total_seconds()
    vehicle_monitoring_counts[delta] += 1

    # Vehicle Activity -> Recorded At Time
    activity_count = 0
    for element in vehicle_monitoring_delivery.findall(
        '{http://www.siri.org.uk/siri}VehicleActivity/' +
        '{http://www.siri.org.uk/siri}RecordedAtTime'):
        timestamp = element.text
        vehicle_activity_timestamp = arrow.get(timestamp)
        delta = (vehicle_monitoring_timestamp - vehicle_activity_timestamp).total_seconds()
        vehicle_activity_deltas.append(delta)
        vehicle_activity_counts[delta] += 1
        activity_count += 1

        if delta < 0 or delta > 15*60:
            print("Negative or large reporting delta in %s of %s" % (filename, delta))

    file_activities_count[activity_count] +=1
    file_activities.append(activity_count)

for i in sorted(service_delivery_counts.keys()):
    print("%s: %s" % (i, service_delivery_counts[i]))

print()

for i in sorted(vehicle_monitoring_counts.keys()):
    print("%s: %s" % (i, vehicle_monitoring_counts[i]))

print()

for i in sorted(vehicle_activity_counts.keys()):
    print("%s: %s" % (i, vehicle_activity_counts[i]))

print()

series = pandas.Series.from_array(vehicle_activity_deltas)
print(series.describe(percentiles=[0.25,0.5,0.75,0.9, 0.99]))

print()

for i in sorted(file_activities_count.keys()):
    print("%s: %s" % (i, file_activities_count[i]))

print()

series = pandas.Series.from_array(file_activities)
print(series.describe(percentiles=[0.25,0.5,0.75,0.9, 0.99]))
