from enum import Enum
from typing import Optional
from dataclasses import dataclass, field

from energytt_platform.serialize import Serializable


class TechnologyType(Enum):
    """
    System-wide labels of known technologies.
    """
    coal = 'coal'
    nuclear = 'nuclear'
    solar = 'solar'
    wind = 'wind'


@dataclass
class Technology(Serializable):
    """
    A technology described by the standard described in the
    EECS Rules Fact Sheet 5: TYPES OF ENERGY INPUTS AND TECHNOLOGIES
    """
    type: TechnologyType
    tech_code: str
    fuel_code: str

