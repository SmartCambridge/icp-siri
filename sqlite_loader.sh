#!/bin/bash

#input='examples/2017-04-26/ examples/2017-08-30/ examples/2017-09-04/'
input='examples/2017-04-26/'
#input='one_file/'
database='activity.sqlite'

tmp=$(mktemp .data-XXXXXX)

./sqlite_loader.py ${input} > "${tmp}"

sqlite3 "${database}" <<EOF
DROP TABLE IF EXISTS activity;
CREATE TABLE activity (
    SerialNo                 int,
    RecievedTimestamp        timestamptz,
    RecordedAtTime           timestamptz,
    ValidUntilTime           timestamptz,
    VehicleMonitoringRef     text,
    LineRef                  text,
    DirectionRef             text,
    DataFrameRef             int,
    DatedVehicleJourneyRef   int,
    PublishedLineName        text,
    OperatorRef              text,
    VehicleFeatureRef        text,
    OriginRef                text,
    OriginName               text,
    DestinationRef           text,
    DestinationName          text,
    OriginAimedDepartureTime timestamptz,
    Monitored                text,
    InPanic                  text,
    Longitude                real,
    Latitude                 real,
    Bearing                  int,
    Delay                    text,
    VehicleRef               text
    );
.separator |
.import ${tmp} activity
SELECT count(*) FROM activity;
EOF

rm "${tmp}"
