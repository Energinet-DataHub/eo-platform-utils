from dataclasses import dataclass

from src.origin.bus import Message
from src.origin.models.delegates import MeteringPointDelegate


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
