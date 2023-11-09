
begin;

create table if not exists station (
    id serial primary key not null,
    meteostat_id varchar(5) not null, 
    name varchar(128) not null, 
    country varchar(2) not null, 
    region varchar(4),
    wmo varchar(5),
    icao varchar(4),
    latitude double precision, 
    longitude double precision,
    elevation double precision,
    timezone varchar(30),
    hourly_start date,
    hourly_end date,
    
    updated_on timestamptz default now(), 

    unique(meteostat_id)
);


create table if not exists weathermeasurement(
    id integer primary key not null,
    label varchar(4) check (
        label in ('temp', 'dwpt', 'rhum', 'tavg', 'tmin', 'tmax')
    ),
    unit varchar(64),
    updated_on timestamptz default now(),
    
    unique(label)
);



create table if not exists normalizedweatherrecord(
    id serial primary key not null,
    station_id integer not null, 
    weathermeasurement_id integer not null,
    month integer not null, 
    value double precision not null,
    updated_on timestamptz default now(),
    
    foreign key(station_id) references station(id) on delete cascade,
    foreign key(weathermeasurement_id) references weathermeasurement(id) on delete restrict,
    unique(station_id, weathermeasurement_id, month)
);



create table if not exists isdrecord(
    id serial primary key not null,
    timestamp timestamptz not null, 
    station_id integer not null, 
    weathermeasurement_id integer not null,
    value double precision, 
    updated_on timestamptz default now(),


    foreign key(station_id) references station(id) on delete cascade,
    foreign key(weathermeasurement_id) references weathermeasurement(id) on delete restrict,

    unique(timestamp, station_id, weathermeasurement_id)
);


select create_hypertable('isdrecord', 'timestamp');



insert into weathermeasurement(id, unit, label)
values
(1, 'degree_F', 'temp'),
(2, 'degree_F', 'tavg'),
(3, 'degree_F', 'tmin'),
(4, 'degree_F', 'tmax'),
(5, 'degree_F', 'dwpt'),
(6, 'percent', 'rhum');

end;