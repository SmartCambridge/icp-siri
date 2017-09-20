.print Monitored values
select distinct(Monitored) from activity;

.print
.print InPanic values
select distinct(InPanic)  from activity;

.print
.print DirectionRef values
select distinct(DirectionRef) from activity;

.print
.print OperatorRef values
select distinct OperatorRef as x from activity order by x;

.print
.print VehicleMonitoringRef values
select distinct VehicleMonitoringRef as x from activity order by x;

.print
.print LineRef values
select OperatorRef, LineRef from activity group by OperatorRef, LineRef order by OperatorRef, LineRef;

.print
.print DataFrameRef values
select distinct DataFrameRef as x from activity order by x;

.print
.print DatedVehicleJourneyRef values
select distinct DatedVehicleJourneyRef as x from activity order by cast(x as integer);

.print
.print OriginRef values
select count(distinct OriginRef) from activity;

.print
.print DestinationRef values
select count(distinct DestinationRef) from activity;

.print
.print VehicleFeatureRef values
select distinct VehicleFeatureRef from activity;

.print
.print Latitude values
select min(cast(Latitude as float)), max(cast(Latitude as float)) from activity;

.print
.print Longitude values
select min(cast(Longitude as float)), max(cast(Longitude as float)) from activity;

.print
.print Non-matching RecordedAtTime and ValidUntilTime
select * from activity where RecordedAtTime <> ValidUntilTime;

.print
.print Bering values
select min(cast(Bearing as float)), max(cast(Bearing as float)) from activity;

.print
.print Non-matching LineRef vs PublishedLineName
select * from activity where LineRef <> PublishedLineName;

.print
.print Any activities where DatedVehicleJourneyRef relates to more than
.print one journey
select date(RecordedAtTime), DatedVehicleJourneyRef, OperatorRef,
LineRef, OriginRef, OriginAimedDepartureTIme,
count(distinct(DatedVehicleJourneyRef)) as count from activity group by
date(RecordedAtTime), DatedVehicleJourneyRef, OperatorRef, LineRef,
OriginRef, OriginAimedDepartureTime having count <> 1 order by
date(RecordedAtTime), DatedVehicleJourneyRef;
