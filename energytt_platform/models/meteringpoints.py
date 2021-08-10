from typing import Optional
from dataclasses import dataclass, field

from energytt_platform.serialize import Serializable

from .technologies import Technology
from .common import EnergyDirection, Address


MeteringPointType = EnergyDirection


@dataclass
class MeteringPoint(Serializable):
    """
    A single Metering Point.
    """
    gsrn: str
    sector: Optional[str] = field(default=None)
    type: Optional[MeteringPointType] = field(default=None)
    technology_code: Optional[str] = field(default=None)
    fuel_code: Optional[str] = field(default=None)
    # technology: Optional[Technology] = field(default=None)
    address: Optional[Address] = field(default=None)
