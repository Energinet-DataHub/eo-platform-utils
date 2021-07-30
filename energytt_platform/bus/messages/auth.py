from dataclasses import dataclass

from energytt_platform.serialize import Serializable


@dataclass
class UserCreated(Serializable):
    pass


@dataclass
class UserProfileUpdated(Serializable):
    pass


@dataclass
class UserDeleted(Serializable):
    pass


@dataclass
class UserConcentGiven(Serializable):
    pass


@dataclass
class UserConcentRevoked(Serializable):
    pass

@dataclass
class UserOnboarded(Serializable):
    """
    A new user has been onboarded to the system.
    """
    subject: str
    name: str