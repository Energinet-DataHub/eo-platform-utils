from dataclasses import dataclass

from src.origin.bus import Message
from src.origin.models.tech import Technology, TechnologyCodes


@dataclass
class TechnologyUpdate(Message):
    """
    A Technology has been added or updated.
    """
    technology: Technology


@dataclass
class TechnologyRemoved(Message):
    """
    TODO
    """
    codes: TechnologyCodes
