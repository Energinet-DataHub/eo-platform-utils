from dataclasses import dataclass

from origin_platform.bus import Message


@dataclass
class UserOnboarded(Message):
    """
    A new user has been onboarded to the system.
    """
    subject: str
