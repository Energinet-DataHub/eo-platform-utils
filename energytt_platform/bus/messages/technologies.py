from dataclasses import dataclass

from energytt_platform.serialize import Serializable
from energytt_platform.models.technologies import Technology


@dataclass
class TechnologyUpdate(Serializable):
    """
    An update to a Technology.
    """
    technology: Technology
