from datetime import datetime
from dataclasses import dataclass


@dataclass
class Measurement:
    gsrn: str
    amount: int
    begin: datetime
    end: datetime


@dataclass
class NewMeasurementMessage:
    measurement: Measurement
