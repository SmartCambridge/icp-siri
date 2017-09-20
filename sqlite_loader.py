#!/usr/bin/env python3

import arrow
import xml.etree.ElementTree as ET
import os
import sys
import re

ns = { 'siri': 'http://www.siri.org.uk/siri' }

tags = ['RecordedAtTime',
        'ValidUntilTime',
        'VehicleMonitoringRef',
        'MonitoredVehicleJourney/LineRef',
        'MonitoredVehicleJourney/DirectionRef',
        'MonitoredVehicleJourney/FramedVehicleJourneyRef/DataFrameRef',
        'MonitoredVehicleJourney/FramedVehicleJourneyRef/DatedVehicleJourneyRef',
        'MonitoredVehicleJourney/PublishedLineName',
        'MonitoredVehicleJourney/OperatorRef',
        'MonitoredVehicleJourney/VehicleFeatureRef',
        'MonitoredVehicleJourney/OriginRef',
        'MonitoredVehicleJourney/OriginName',
        'MonitoredVehicleJourney/DestinationRef',
        'MonitoredVehicleJourney/DestinationName',
        'MonitoredVehicleJourney/OriginAimedDepartureTime',
        'MonitoredVehicleJourney/Monitored',
        'MonitoredVehicleJourney/InPanic',
        'MonitoredVehicleJourney/VehicleLocation/Longitude',
        'MonitoredVehicleJourney/VehicleLocation/Latitude',
        'MonitoredVehicleJourney/Bearing',
        'MonitoredVehicleJourney/Delay',
        'MonitoredVehicleJourney/VehicleRef'
       ]

def lookup_tag(tag, base):
  tag = 'siri:' + tag
  tag = re.sub(r'/', '/siri:', tag)
  try:
    return base.find(tag, ns).text
  except AttributeError:
    return 'NULL'

for directory in sys.argv[1:]:

  for file in os.listdir(os.fsencode(directory)):
    filename = os.path.join(directory, os.fsdecode(file))
    if not filename.endswith(".xml"):
        continue

    # Reciept timestamp, from filename
    basename = os.path.basename(filename)
    timestamp = basename[:10]
    our_timestamp = arrow.get(timestamp).format()

    tree = ET.parse(filename)
    root = tree.getroot()

    serial = 0;
    base = 'siri:ServiceDelivery/siri:VehicleMonitoringDelivery/siri:VehicleActivity'
    for report in root.findall(base, ns):

      result = [str(serial),our_timestamp]
      for tag in tags:
        result.append(lookup_tag(tag,report))
      print('|'.join(result))
      serial += 1
