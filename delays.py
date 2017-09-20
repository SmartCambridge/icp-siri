#!/usr/bin/env python3

import arrow
import xml.etree.ElementTree as ET
import os
import sys

for directory in sys.argv[1:]:

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
            print(delta)
