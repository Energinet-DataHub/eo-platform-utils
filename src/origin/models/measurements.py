from datetime import datetime
from dataclasses import dataclass

from origin.serialize import Serializable

from .common import EnergyDirection


MeasurementType = EnergyDirection


@dataclass
class Measurement(Serializable):
    """Class to store the parameters for the measurement."""

    id: str
    gsrn: str
    amount: int
    begin: datetime
    end: datetime
