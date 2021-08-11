from typing import Optional
from dataclasses import dataclass, field

from energytt_platform.bus import Message
from energytt_platform.models.common import Address
from energytt_platform.models.technologies import TechnologyCodes
from energytt_platform.models.meteringpoints import \
    MeteringPoint, MeteringPointBasics, MeteringPointDelegate


@dataclass
class MeteringPointAdded(Message):
    """
    A MeteringPoint has either been added to the system,
    or an existing MeteringPoint has had its details updated.
    """
    meteringpoint: MeteringPoint


@dataclass
class MeteringPointUpdated(Message):
    """
    A MeteringPoint has either been added to the system,
    or an existing MeteringPoint has had its details updated.
    """
    gsrn: str
    basics: Optional[MeteringPointBasics] = field(default=None)
    technology: Optional[TechnologyCodes] = field(default=None)
    address: Optional[Address] = field(default=None)


@dataclass
class MeteringPointTechnologyUpdated(Message):
    """
    A MeteringPoint has either been added to the system,
    or an existing MeteringPoint has had its details updated.
    """
    gsrn: str
    tech_code: str
    fuel_code: str


@dataclass
class MeteringPointRemoved(Message):
    """
    A MeteringPoint has been remove from the system.
    # TODO Advice to perform Clean-up?
    """
    gsrn: str


# -- Delegate ----------------------------------------------------------------


@dataclass
class MeteringPointDelegateGranted(Message):
    """
    An actor (identified by its subject) has been delegated
    access to a MeteringPoint.
    """
    delegate: MeteringPointDelegate


@dataclass
class MeteringPointDelegateRevoked(Message):
    """
    An actor (identified by its subject) has had its delegated
    access to a MeteringPoint revoked.
    """
    delegate: MeteringPointDelegate
