from datetime import datetime
from enum import Enum
from dataclasses import dataclass
from typing import List, Dict, Union

from energytt_platform.serialize import Serializable
from energytt_platform.arithmetic import ArithmeticDict
from energytt_platform.models.technologies import TechnologyLabel


# -- Common ------------------------------------------------------------------


TEmissionValue = Union[int, float]


class EmissionLabel(Enum):
    """
    System-wide labels of known emission types.
    """
    CO2 = 'CO2'
    SO2 = 'SO2'


class EmissionValues(ArithmeticDict, Dict[EmissionLabel, TEmissionValue]):
    """
    Represents a set of emissions indexed by name
    """
    pass


# -- Residual Mix emissions --------------------------------------------------


@dataclass
class ResidualMixEmissions(Serializable):
    """
    Describes emissions in the general mix within a single
    sector (pricing area), and in a specific time-frame.
    """
    sector: str  # Sector where energy is consumed
    begin: datetime
    end: datetime
    emissions: EmissionValues  # g/Wh


# -- Residual Mix technologies -----------------------------------------------

@dataclass
class ResidualMixTechnology(Serializable):
    """
    Describes a part of the residual mix consumption, specifically
    how large a percentage of the total energy consumed originates
    from a single type of technology.
    """
    technology: TechnologyLabel
    percent: float
    sector: str  # Sector where energy is produced


@dataclass
class ResidualMixTechnologyDistribution(Serializable):
    """
    Describes the distribution of technologies used to produce energy
    in the residual mix within a single sector (pricing area),
    and in a specific time-frame.
    """
    sector: str  # Sector where energy is consumed
    begin: datetime
    end: datetime

    # Distribution of produced energy on technologies.
    # The list is unique on (technology, sector) (composite key).
    # The sum of ResidualMixTechnology.percent MUST be exactly 1.0.
    technologies: List[ResidualMixTechnology]
