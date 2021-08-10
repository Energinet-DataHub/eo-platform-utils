from typing import Optional
from dataclasses import dataclass, field

from energytt_platform.serialize import Serializable

from .technologies import Technology
from .common import EnergyDirection, Address


MeteringPointType = EnergyDirection


@dataclass
class MeteringPointIdentity(Serializable):
    """
    TODO
    """
    gsrn: str


@dataclass
class MeteringPointBasics(Serializable):
    """
    TODO
    """
    sector: Optional[str] = field(default=None)
    type: Optional[MeteringPointType] = field(default=None)


@dataclass
class MeteringPoint(Serializable):
    """
    TODO
    """
    gsrn: str
    type: Optional[MeteringPointType] = field(default=None)
    sector: Optional[str] = field(default=None)
    technology: Optional[Technology] = field(default=None)
    address: Optional[Address] = field(default=None)


@dataclass
class MeteringPoint2(
    Address,
    MeteringPointBasics,
    Technology,
    MeteringPointIdentity,
):
    """
    TODO
    """

    @property
    def technology_codes(self) -> TechnologyCodes:
        return TechnologyCodes.create_from(self)

    @property
    def address(self) -> Address:
        return Address.create_from(self)


@dataclass
class MeteringPointDelegate(Serializable):
    """
    An actor (identified by its subject) who has been delegated
    access to a MeteringPoint (identified by its GSRN number).
    """
    gsrn: str
    subject: str
