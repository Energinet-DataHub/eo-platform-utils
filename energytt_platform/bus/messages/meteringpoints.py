from dataclasses import dataclass

from energytt_platform.serialize import Serializable
from energytt_platform.models.meteringpoints import MeteringPoint


@dataclass
class NewMeteringPoint(Serializable):
    """
    A new MeteringPoint has been added to the system.
    """
    meteringpoint: MeteringPoint
