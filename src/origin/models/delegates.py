from dataclasses import dataclass

from origin.serialize import Serializable


@dataclass
class MeteringPointDelegate(Serializable):
    """
    Delegation of meteringPoints to actors.

    An actor (identified by its subject) who has been delegated
    access to a MeteringPoint (identified by its GSRN number).
    """

    subject: str
    gsrn: str

    # TODO Define time period (???)
