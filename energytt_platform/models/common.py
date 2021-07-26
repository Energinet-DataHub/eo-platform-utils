from enum import Enum


class Resolution(Enum):
    HOUR = 'HOUR'
    DAY = 'DAY'
    MONTH = 'MONTH'
    YEAR = 'YEAR'


class MeasurementType(Enum):
    PRODUCTION = 'PRODUCTION'
    CONSUMPTION = 'CONSUMPTION'
