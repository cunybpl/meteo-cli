#! /bin/bash 
set -e 

PG_URI=$PG_URI
STATION_ID=$STATION_ID
meteo-cli station -i $STATION_ID > station.csv 
meteo-cli normals -i $STATION_ID -m tavg -m tmin -m tmax > norms.csv
meteo-cli isd -i $STATION_ID -m temp -s 2014-01-01 -e 2023-11-01 > isd.csv


# -- https://stackoverflow.com/questions/8910494/how-to-update-selected-rows-with-values-from-a-csv-file-in-postgres/8910810#8910810
psql $PG_URI << EOF 
begin;

create temp table _station_tmp (like station including defaults)
on commit drop; 

create temp table _normals_tmp (
    station varchar not null, 
    weathermeasurement varchar not null, 
    month integer not null, 
    value double precision not null
) on commit drop; 


create temp table _isd_tmp (
    timestamp timestamptz not null,
    station varchar,
    weathermeasurement varchar not null,
    value double precision not null
) on commit drop;


create index tmp_isd_idx on _isd_tmp(timestamp, station, weathermeasurement);
analyze _isd_tmp;

\copy _station_tmp (meteostat_id, name, country, region, wmo,icao,latitude,longitude,elevation,timezone,hourly_start,hourly_end) from 'station.csv' delimiter ',' csv header;

insert into station 
select * from _station_tmp
on conflict(meteostat_id) do nothing;

\copy _normals_tmp (station, weathermeasurement, month, value) from 'norms.csv' delimiter ',' csv header;

insert into normalizedweatherrecord (station_id, weathermeasurement_id, month, value)
select
    (select s.id from station s where s.meteostat_id = _t.station) as station_id,
    (select w.id from weathermeasurement w where w.label = _t.weathermeasurement) as weathermeasurement_id,
    _t.month,
    _t.value
from _normals_tmp _t
on conflict (station_id, weathermeasurement_id, month) do update
set value = excluded.value;


\copy _isd_tmp (timestamp, station, weathermeasurement, value) from 'isd.csv' delimiter ',' csv header;

insert into isdrecord (timestamp, station_id, weathermeasurement_id, value)
select
    _t.timestamp,
    (select s.id from station s where s.meteostat_id = _t.station) as station_id,
    (select w.id from weathermeasurement w where w.label = _t.weathermeasurement) as weathermeasurement_id,
    _t.value
from _isd_tmp _t
on conflict (timestamp, station_id, weathermeasurement_id) do update
set value = excluded.value;

end; 
EOF

rm isd.csv norms.csv station.csv