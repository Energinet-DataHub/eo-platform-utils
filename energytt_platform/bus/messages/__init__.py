from energytt_platform.bus import message_registry

from .auth import UserOnboarded
from .tech import TechnologyUpdate, TechnologyRemoved
from .measurements import MeasurementAdded
from .meteringpoints import (
    MeteringPointAdded,
    MeteringPointRemoved,
    MeteringPointTechnologyUpdated,
    MeteringPointAddressUpdated,
    MeteringPointDelegateGranted,
    MeteringPointDelegateRevoked,
)


message_registry.add(

    # Authentication
    UserOnboarded,

    # Technology
    TechnologyUpdate,
    TechnologyRemoved,

    # Measurements
    MeasurementAdded,

    # MeteringPoints
    MeteringPointAdded,
    MeteringPointRemoved,
    MeteringPointTechnologyUpdated,
    MeteringPointAddressUpdated,
    MeteringPointDelegateGranted,
    MeteringPointDelegateRevoked,

)
