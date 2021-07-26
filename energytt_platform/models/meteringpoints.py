from dataclasses import dataclass

from energytt_platform.serialize import Serializable

from .common import MeasurementType


@dataclass
class MeteringPoint(Serializable):
    """
    A single Metering Point.

    TODO Add physical address
    """
    type: MeasurementType
    gsrn: str
    sector: str
    technology_code: str
    fuel_code: str
