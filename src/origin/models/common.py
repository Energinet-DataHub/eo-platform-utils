from enum import Enum
from serpyco import field
from dataclasses import dataclass
from datetime import date, datetime
from typing import Optional, Generic, TypeVar, List

from origin.serialize import Serializable


# -- Data objects ------------------------------------------------------------


class EnergyDirection(Enum):
    """Enumeration to bound the constant values to the symbolic name."""

    PRODUCTION = 'production'
    CONSUMPTION = 'consumption'


@dataclass
class Address(Serializable):
    """
    Class to store the parameters the address parameters.

    International standard for addresses in Denmark
    https://danmarksadresser.dk/adressedata/standarder-for-adresser
    """

    street_code: Optional[str] = field(default=None)
    street_name: Optional[str] = field(default=None)
    building_number: Optional[str] = field(default=None)
    floor_id: Optional[str] = field(default=None)
    room_id: Optional[str] = field(default=None)
    post_code: Optional[str] = field(default=None)
    city_name: Optional[str] = field(default=None)
    city_sub_division_name: Optional[str] = field(default=None)
    municipality_code: Optional[str] = field(default=None)
    location_description: Optional[str] = field(default=None)

    def __str__(self) -> str:
        """Create a string representation of the address."""

        return self.format()

    def format(self, separator: str = '\n') -> str:
        """Create a string representation of the address."""

        return separator.join(self.parts)

    @property
    def parts(self) -> List[str]:
        """Create a empty string for the representation of the address."""

        return []


# -- Value Ranges ------------------------------------------------------------


@dataclass
class DateRange(Serializable):
    """A range of dates."""

    from_: Optional[date] = field(default=None, dict_key='from')
    to_: Optional[date] = field(default=None, dict_key='to')


@dataclass
class DateTimeRange(Serializable):
    """A range of datetimes."""

    from_: Optional[datetime] = field(default=None, dict_key='from')
    to_: Optional[datetime] = field(default=None, dict_key='to')


# -- API & Querying ----------------------------------------------------------


TOrderKey = TypeVar('TOrderKey', bound=Enum)


class Order(Enum):
    """Enumeration to bound the constant values to the symbolic name."""

    ASC = 'asc'
    DESC = 'desc'


@dataclass
class ResultOrdering(Serializable, Generic[TOrderKey]):
    """Ordering of query results."""

    key: Optional[TOrderKey] = field(default=None)
    order: Order = field(default=Order.ASC)

    @property
    def asc(self) -> bool:
        """Ordering of the ASC result."""

        return self.order is Order.ASC

    @property
    def desc(self) -> bool:
        """Ordering of the DESC result."""

        return self.order is Order.DESC
