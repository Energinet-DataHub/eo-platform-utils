from energytt_platform.bus import message_registry

from .auth import UserOnboarded
from .technologies import TechnologyUpdate, TechnologyRemoved
from .measurements import MeasurementAdded
from .meteringpoints import (
    MeteringPointAdded,
    MeteringPointUpdated,
    # MeteringPointTechnologyUpdated,
    # MeteringPointAddressUpdated,
    MeteringPointRemoved,
    # MeteringPointMetaDataUpdate,
    MeteringPointDelegateGranted,
    MeteringPointDelegateRevoked,
)


message_registry.add(
    UserOnboarded,
    TechnologyUpdate,
    TechnologyRemoved,
    MeasurementAdded,
    MeteringPointAdded,
    MeteringPointUpdated,
    # MeteringPointTechnologyUpdated,
    # MeteringPointAddressUpdated,
    MeteringPointRemoved,
    # MeteringPointMetaDataUpdate,
    MeteringPointDelegateGranted,
    MeteringPointDelegateRevoked,
)
