from datetime import datetime
from typing import List, Dict
from dataclasses import dataclass

from energytt_platform.serialize import Serializable
from energytt_platform.models.technologies import TechnologyLabel


@dataclass
class ResidualMixTechnology(Serializable):
    """
    Describes a part of emissions in the general mix, specifically
    how large a percentage of the total energy from a single technology.
    """
    technology: TechnologyLabel
    percent: float
    sector: str  # Sector where energy is produced


@dataclass
class ResidualMixData(Serializable):
    """
    Describes emissions in the general mix, and its distribution
    among different technologies, within a single sector (pricing area).
    """
    sector: str  # Sector where energy is consumed
    begin: datetime
    end: datetime
    emissions: Dict[str, float]  # g/Wh

    # Technologies unique on: (technology, sector) (composite key)
    technologies: List[ResidualMixTechnology]
