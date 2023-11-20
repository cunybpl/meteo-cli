import datetime

import pydantic
from typing import List, Any
from meteostat import Stations  # type: ignore

from . import base


class Station(base.MeteoEntity):
    meteostat_id: str = pydantic.Field(validation_alias="id")
    name: str
    country: str
    region: str | None = None
    wmo: str | None = None
    icao: str | None = None
    latitude: float | None = None
    longitude: float | None = None
    elevation: float | None = None
    timezone: str | None = None
    hourly_start: datetime.datetime | None = None
    hourly_end: datetime.datetime | None = None


class StationOutput(base.CsvOut[Station]):
    data: List[Station]


def _fetch(
    id_: str | None = None, country: str = "US", state: str = "NY"
) -> StationOutput:
    """Use meteostat to get a region. Filter by id if provided

    Args:
        id_ (str | None, optional): _description_. Defaults to None.
        country (str, optional): _description_. Defaults to "US".
        state (str, optional): _description_. Defaults to "NY".

    Returns:
        List[Dict[str, Any]]: _description_
    """
    stations = Stations()
    local = stations.region(country=country, state=state)

    data: List[dict[str, Any]] = (
        local.fetch().reset_index().to_dict("records", index=True)
    )
    if id_:
        return StationOutput.model_validate(
            {"data": list(filter(lambda item: item["id"] == id_, data))}
        )
    else:
        return StationOutput(data=data)  # type:ignore


def entrypoint(id_: str | None = None, country: str = "US", state: str = "NY") -> None:
    s = _fetch(id_, country, state)
    s.out()
