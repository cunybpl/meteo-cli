import datetime
import pydantic
from typing import List
from meteostat import Hourly, units  # type: ignore

from . import base
from typing import List


class Isd(base.MeteoEntity):
    timestamp: datetime.datetime = pydantic.Field(validation_alias="time")
    station: str
    weathermeasurement: str
    value: float


class IsdOutput(base.CsvOut[Isd]):
    data: List[Isd]


def _fetch(
    id_: str,
    measures: List[str],
    start: datetime.datetime,
    end: datetime.datetime,
) -> IsdOutput:
    assert id_ is not None

    hourly = Hourly(id_, start, end)
    hourly.convert(units=units.imperial)
    df = (
        hourly.fetch()
        .reset_index()
        .melt(id_vars=["time"], var_name="weathermeasurement")
    )
    df = df[(df.weathermeasurement.isin(measures))]
    df["station"] = id_

    return IsdOutput.model_validate({"data": df.to_dict("records")})


def entrypoint(
    meteostat_id: str,
    measures: list[str],
    start: datetime.datetime,
    end: datetime.datetime,
) -> None:
    _fetch(meteostat_id, measures, start, end).out()
