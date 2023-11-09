import pydantic
import abc
import sys
import csv
from typing import TypeVar, Generic, Sequence
import enum


class NormsWeatherMeasurementEnum(str, enum.Enum):
    tavg = "tavg"
    tmin = "tmin"
    tmax = "tmax"


class IsdWeatherMeasurementEnum(str, enum.Enum):
    temp = "temp"
    dwpt = "dwpt"
    rhum = "rhum"


class MeteoBase(pydantic.BaseModel, abc.ABC):
    model_config = pydantic.ConfigDict(from_attributes=True)


class MeteoEntity(MeteoBase):
    def fields(self):
        return self.model_fields


MeteoEntityT = TypeVar("MeteoEntityT", bound=MeteoEntity)


class CsvOut(pydantic.BaseModel, Generic[MeteoEntityT]):
    data: Sequence[MeteoEntityT] = []

    def out(self):
        if len(self.data) > 0:
            fieldnames = self.data[0].fields()
            writer = csv.DictWriter(f=sys.stdout, fieldnames=fieldnames)
            writer.writeheader()
            for d in self.data:
                writer.writerow(d.model_dump())
