from enum import Enum
from dataclasses import dataclass

from origin.serialize import Serializable


class TechnologyType(Enum):
    """System-wide labels of known technologies."""

    COAL = 'coal'
    NUCLEAR = 'nuclear'
    SOLAR = 'solar'
    WIND = 'wind'


@dataclass
class TechnologyCodes(Serializable):
    """
    Technology Code and Fuel Source Code for Electricity Production.

    Codes are described in the standard EECS Rules Fact Sheet 5: TYPES OF
    ENERGY INPUTS AND TECHNOLOGIES.
    """

    tech_code: str
    fuel_code: str


@dataclass
class Technology(Serializable):
    """
    Technology description from the standard EECS Rules Fact Sheet 5.

    A technology described by the standard described in the EECS Rules Fact
    Sheet 5: TYPES OF ENERGY INPUTS AND TECHNOLOGIES.
    """

    tech_code: str
    fuel_code: str
    type: TechnologyType
