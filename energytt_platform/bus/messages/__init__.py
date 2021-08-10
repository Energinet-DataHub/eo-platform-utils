from energytt_platform.bus import message_registry

from .auth import UserOnboarded
from .technologies import TechnologyUpdate
from .measurements import MeasurementAdded
from .meteringpoints import (
    MeteringPointAdded,
    MeteringPointUpdated,
    MeteringPointRemoved,
    MeteringPointMetaDataUpdate,
)


message_registry.add(
    UserOnboarded,
    MeasurementAdded,
    MeteringPointAdded,
    MeteringPointRemoved,
    MeteringPointMetaDataUpdate,
)
