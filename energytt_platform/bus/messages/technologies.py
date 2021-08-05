from dataclasses import dataclass

from energytt_platform.serialize import Serializable
from energytt_platform.models.common import Technology


@dataclass
class TechnologyUpdate(Serializable):
    """
    An update to a Technology.
    """
    technology: Technology
