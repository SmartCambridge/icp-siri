#!/usr/bin/env python3

import arrow
import collections
import xml.etree.ElementTree as ET
import os
import sys
import pandas
import csv

csv_writer = csv.writer(sys.stdout)
csv_writer.writerow(('day','count','mean','std','min','25%','50%','75%','90%','99%', 'max'))

for directory in sys.argv[1:]:

    vehicle_activity_deltas = []

    for file in os.listdir(os.fsencode(directory)):
        filename = os.path.join(directory, os.fsdecode(file))
        if not filename.endswith(".xml"):
            continue

        # Reciept timestamp, from filename
        basename = os.path.basename(filename)
        timestamp = basename[:10]
        our_timestamp = arrow.get(timestamp)

        tree = ET.parse(filename)
        root=tree.getroot()

        service_delivery = root.find('{http://www.siri.org.uk/siri}ServiceDelivery')
        if service_delivery is None:
            continue
        vehicle_monitoring_delivery = service_delivery.find('{http://www.siri.org.uk/siri}VehicleMonitoringDelivery')
        if vehicle_monitoring_delivery is None:
            continue
        for element in vehicle_monitoring_delivery.findall(
            '{http://www.siri.org.uk/siri}VehicleActivity/' +
            '{http://www.siri.org.uk/siri}RecordedAtTime'):
            timestamp = element.text
            vehicle_activity_timestamp = arrow.get(timestamp)
            delta = (our_timestamp - vehicle_activity_timestamp).total_seconds()
            vehicle_activity_deltas.append(delta)

    if len(vehicle_activity_deltas) > 0:

        series = pandas.Series.from_array(vehicle_activity_deltas)
        #print(series.describe(percentiles=[0.25,0.5,0.75,0.9, 0.99]))

        csv_writer.writerow((our_timestamp.to('local').format("YYYY-MM-DD"),
            series.count(),
            series.mean(),
            series.std(),
            series.min(),
            series.quantile(0.25),
            series.quantile(0.5),
            series.quantile(0.75),
            series.quantile(0.90),
            series.quantile(0.99),
            series.max()))
