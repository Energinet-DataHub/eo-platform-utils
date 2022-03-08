from dataclasses import dataclass

from origin.bus import Message
from origin.models.delegates import MeteringPointDelegate


@dataclass
class MeteringPointDelegateGranted(Message):
    """
    An actor has been delegated access to a MeteringPoint.

    An actor is identified by its subject
    """

    delegate: MeteringPointDelegate


@dataclass
class MeteringPointDelegateRevoked(Message):
    """
    An actor has had its delegated access to a MeteringPoint revoked.

    An actor is identified by its subject.
    """

    delegate: MeteringPointDelegate
