from dataclasses import dataclass

from energytt_platform.bus import Message
from energytt_platform.models.tech import Technology


@dataclass
class TechnologyUpdate(Message):
    """
    A Technology has been added or updated.
    """
    technology: Technology


@dataclass
class TechnologyDeleted(Message):
    """
    TODO
    """
    tech_code: str
    fuel_code: str
