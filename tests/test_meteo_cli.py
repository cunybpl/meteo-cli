from meteo_cli import station, isd, normals
import datetime


def test_station_fetch():
    meteo_station_id = "72503"
    res = station._fetch(meteo_station_id, "US", "NY")
    assert res.data

    station_ = res.data.pop()
    assert station_.meteostat_id == meteo_station_id
    assert station_.name == "LaGuardia Airport"
    assert station_.country == "US"
    assert station_.region == "NY"


def test_station_entrypoint(capsys):
    meteo_station_id = "72503"
    station.entrypoint(meteo_station_id)
    captured = capsys.readouterr()
    csv_out = captured.out
    csv_head = "meteostat_id,name,country,region,wmo,icao,latitude,longitude,elevation,timezone,hourly_start,hourly_end"
    assert csv_head in csv_out
    assert meteo_station_id in csv_out
    assert "LaGuardia Airport" in csv_out
    assert csv_out.count("\n") == 2


def test_isd_fetch():
    meteo_station_id = "72503"
    start = datetime.datetime(2020, 1, 1)
    end = datetime.datetime(2020, 1, 2)
    res = isd._fetch(meteo_station_id, ["temp"], start, end)

    assert res.data
    assert len(res.data) == 25

    isd_ = res.data.pop()
    assert isd_.weathermeasurement == "temp"
    assert isd_.station == "72503"
    assert isd_.value

    res = isd._fetch(meteo_station_id, ["dwpt", "rhum"], start, end)

    assert res.data
    assert len(res.data) == 50

    dwpt_ = [i for i in res.data if i.weathermeasurement == "dwpt"]
    assert len(dwpt_) == 25
    rhum_ = [i for i in res.data if i.weathermeasurement == "rhum"]
    assert len(rhum_) == 25


def test_isd_entrypoint(capsys):
    meteo_station_id = "72503"
    start = datetime.datetime(2020, 1, 1)
    end = datetime.datetime(2020, 1, 2)
    isd.entrypoint(meteo_station_id, ["temp"], start, end)

    captured = capsys.readouterr()
    csv_out = captured.out
    csv_head = "timestamp,station,weathermeasurement,value"
    assert csv_head in csv_out
    assert "temp" in csv_out
    assert start.strftime("%Y-%m-%d %H:%M:%S") in csv_out
    assert csv_out.count("\n") == 26  # header + 25 rows


def test_normals_fetch():
    meteo_station_id = "72503"

    res = normals._fetch(meteo_station_id, ["tavg"])
    assert res.data
    assert len(res.data) == 12

    normals_ = res.data.pop()
    assert normals_.station == meteo_station_id
    assert normals_.weathermeasurement == "tavg"
    assert normals_.month
    assert normals_.value

    res = normals._fetch(meteo_station_id)
    assert res.data
    assert len(res.data) == 36


def test_normals_entrypoint(capsys):
    meteo_station_id = "72503"
    normals.entrypoint(meteo_station_id, ["tavg"], 1991, 2020)

    captured = capsys.readouterr()
    csv_out = captured.out
    csv_head = "station,weathermeasurement,month,value"
    assert csv_head in csv_out
    assert "tavg" in csv_out
    assert csv_out.count("\n") == 13
