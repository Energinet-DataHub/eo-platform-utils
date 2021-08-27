from typing import List
from datetime import datetime
from dataclasses import dataclass

from energytt_platform.serialize import Serializable


# @dataclass
# class OpaqueToken(Serializable):
#     issued: datetime
#     expires: datetime
#     subject: str
#     scope: List[str]
#     on_behalf_of: Optional[str]
#
#     @property
#     def actual_subject(self) -> str:
#         if self.on_behalf_of:
#             return self.on_behalf_of
#         else:
#             return self.subject


@dataclass
class OpaqueToken(Serializable):
    """
    TODO
    """
    issued: datetime
    expires: datetime
    subject: str


@dataclass
class InternalToken(Serializable):
    """
    TODO
    """
    issued: datetime
    expires: datetime
    subject: str
    scope: List[str]


@dataclass
class PointDelegate(Serializable):
    """
    An actor (identified by its subject) who has been delegated
    access to a MeteringPoint (identified by its GSRN number).
    """
    subject: str
    gsrn: str

    # TODO Define time period (???)


# -- Delegates ---------------------------------------------------------------


@dataclass
class MeteringPointDelegate(Serializable):
    """
    An actor (identified by its subject) who has been delegated
    access to a MeteringPoint (identified by its GSRN number).
    """
    subject: str
    gsrn: str

    # TODO Define time period (???)
