import click
import datetime

from . import station, base, normals, isd


@click.group("meteo-cli")
def main() -> None:
    """meteo-cli"""


@main.command("station")
@click.option("-i", "--meteostat_id", type=click.STRING)
@click.option("--country", default="US")
@click.option("--state", default="NY")
def station_(meteostat_id: str | None, country: str, state: str) -> None:
    """Pull station(s) by region. If given the correct meteo id will pull a specific station.

    Ex. $ meteo-cli station 72503
    (for laguardia)
    """
    station.entrypoint(meteostat_id, country, state)


@main.command("normals")
@click.option(
    "-i",
    "--meteostat_id",
    type=click.STRING,
    required=True,
    help="The meteostat_id of the station you are after. Ex. 72503 for LaGuardia",
)
@click.option(
    "-m",
    "--measures",
    type=click.Choice([e.value for e in base.NormsWeatherMeasurementEnum]),
    multiple=True,
    help="Measures to include. Ex. -m tavg -m tmin -m tmax will include all.",
    required=True,
)
@click.option(
    "-s",
    "--start-year",
    type=click.INT,
    default=1991,
    help="Begin getting normalzied data at this year. Default is 1991.",
)
@click.option(
    "-e",
    "--end-year",
    type=click.INT,
    default=2020,
    help="End getting normalzied data at this year. Default is 2020.",
)
def normals_(
    meteostat_id: str, measures: list[str], start_year: int, end_year: int
) -> None:
    """Pull monthly normals from meteo given a meteo id. Our application currently supports tavg, tmin and tmax.
    Default years are 1991 -2020 (most recent). You must also include `-m` measure options. We support
    temperature avg, temperature min and temperature max. We convert these to degrees_F.

    Ex. $ meteo-cli normals 72503 -m tavg -m tmin -m tmax
    (pulls normals for laguardia 1991-2020 for all 3 measures)
    """
    normals.entrypoint(meteostat_id, measures, start_year, end_year)


@main.command("isd")
@click.option(
    "-i",
    "--meteostat_id",
    type=click.STRING,
    required=True,
)
@click.option(
    "-m",
    "--measures",
    type=click.Choice([e.value for e in base.IsdWeatherMeasurementEnum]),
    multiple=True,
    help="Measures to include. Ex. -m temp -m dwpt -m rhum will include all.",
    required=True,
)
@click.option(
    "-s",
    "--start-date",
    type=click.DateTime(formats=["%Y-%m-%d"]),
    required=True,
)
@click.option(
    "-e",
    "--end-date",
    type=click.DateTime(formats=["%Y-%m-%d"]),
    required=True,
)
def isd_(
    meteostat_id: str,
    measures: list[str],
    start_date: datetime.datetime,
    end_date: datetime.datetime,
) -> None:
    """Pull hourly isd data for the given `meteostat_id` between start and end date for the given measures. The `temp` measure
    is converted to degrees_F

    ex. $ meteo-cli isd -i 72503 -s 2020-01-01 -e 2021-01-01 -m temp -m dwpt -m rhum
    (pulls all isd for these 3 measures for laguardia)
    """
    isd.entrypoint(meteostat_id, measures, start_date, end_date)
