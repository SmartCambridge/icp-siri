The Postgres database used by some of the following is created by applying
`pgloader` to the initial SQLite database.

Files
=====

* `one_file/`: directory containing a single example SIRI-VM data file
encoded in XML

* `delays.py`: Read one or more directory names from the
command line. From these, read all `*.xml` files and assume each
contains a collection of SIRI-VM records encoded in XML. For each
record, print the difference between
the event's time (`RecordedAtTime`) and our time of receipt
as encoded in the file name.

* `compare_reciept.py`: Read one or more directory names from the
command line. From these, read all `*.xml` files and assume each
contains one day's worth of SIRI-VM data encoded in XML. Print
a text summary of the differences between
the event's time (`RecordedAtTime`) and our time of receipt
as encoded in the file name.

* `sumarise_reciept.py`: Read one or more directory names from the
command line. From these, read all `*.xml` files and assume each
contains one day's worth of SIRI-VM data encoded in XML. For each
day, print to stdout in CSV summary statistics of the difference between
the event's time (`RecordedAtTime`) and our time of receipt
as encoded in the file name.

* `latencies.csv`: Example output from `sumarise_reciept.py`

* `plotter.py`: Read the file `latencies.csv`, assumed to contain the
output from `sumarise_reciept.py`. Plot the contents.

* `siri_analysis.pdf`: example output from `plotter.py`

* `sqlite_loader.py`: Read one or more directory names from the
command line. From these, read all `*.xml` files and assume each
contains SIRI-VM data encoded in XML. Extract selected fields
and print them to stdout in a format suitable for `sqlite_loader.sh`

* `sqlite_loader.sh`: run `sqlite_loader.py`. load data extracted into
the table `activity` in the SQLite database `activity.sqlite`

* `activity.sqlite`: example SQLite database created by `sqlite_loader.sh`

* `questions.sql`: Extract misc summaries from the data in the SQLite
database created by `sumarise_reciept.py`

* `schema.sql`: Schema for the SQLite database created by
`sumarise_reciept.py`

* `extract_journeys.py`: extract a set of possible journeys from the SQLite
database created by `sqlite_loader.sh`

* `extract_one_journey.py`: extract a particular hard-coded journey from
the SQLite database created by `sqlite_loader.sh`

* `deltas.sql`: from a Postgres version of the SQLite database created by `sqlite_loader.sh`
extract the time (delta) between consecutive position reports for each
journey identified by (vehiclemonitoringref, originref, originaimeddeparturetime)
tuples.

* `deltas.csv`: example output from `deltas.sql`

* `deltas.ods`: LibreOffice spreadsheet of `deltas.csv` data

* `deltas.png`: Plot of the data from `deltas.png`

* `find-dups.sql`: Select records containing duplicated data

* `flag-dups.sql`: set a flag on the second and subsequent record containing
duplicated data in a Postgres version of the SQLite database created by
`sqlite_loader.sh`

* `iterator.py`: Iteratively query a Postgres table of unique journey
data grouping it by all plausible combinations of columns to establish which
combinations are unique (see summary in `Looking-at-journies`)

* `Looking-at-journies`: notes on how to partition SIRI-VM records into
distinct journeys

* `animation/`: directory containing a simple animation of a single bus
journey

* `siri-1.3`: Siri 1.3 documentation and schema

* `siri-1.3.zip`: Source of `siri-1.3`

* `siri_vehicleMonitoring_service.svg`: SVG diagram of SIRI
vehicleMonitoring_service schema

* `siri_summary.md`: Summary of observer characteristics of the SIRI data

* `siri_summary.pdf`: Formatted version of `siri_summary.md`

