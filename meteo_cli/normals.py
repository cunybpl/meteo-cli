from typing import List
from meteostat import Normals, units  # type: ignore

from . import base
from typing import List


class Normal(base.MeteoEntity):
    station: str
    weathermeasurement: str
    month: int
    value: float


class NormalOutput(base.CsvOut[Normal]):
    data: List[Normal]


def _fetch(
    id_: str | None = None,
    measures: List[str] = ["tavg", "tmin", "tmax"],
    start_year: int = 1991,
    end_year: int = 2020,
) -> NormalOutput:
    assert id_ is not None
    norms = Normals(id_, start_year, end_year)
    norms.convert(units=units.imperial)
    df = (
        norms.fetch()
        .reset_index()
        .melt(id_vars=["month"], var_name="weathermeasurement")
    )
    df = df[(df.weathermeasurement.isin(measures))]
    df["station"] = id_

    data = df.to_dict("records")
    return NormalOutput.model_validate({"data": data})


def entrypoint(
    meteostat_id: str, measures: list[str], start_year: int, end_year: int
) -> None:
    _fetch(meteostat_id, measures, start_year, end_year).out()
