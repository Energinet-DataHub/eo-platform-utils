from energytt_platform.bus import message_registry

from .users import UserOnboarded
from .tech import TechnologyUpdate, TechnologyRemoved
from .auth import (
    MeteringPointDelegateGranted,
    MeteringPointDelegateRevoked,
)
from .measurements import (
    MeasurementUpdate,
    MeasurementRemoved,
)
from .meteringpoints import (
    MeteringPointUpdate,
    MeteringPointRemoved,
    MeteringPointTechnologyUpdate,
    MeteringPointAddressUpdate,
)


message_registry.add(

    # Users
    UserOnboarded,

    # Authentication
    MeteringPointDelegateGranted,
    MeteringPointDelegateRevoked,

    # Technology
    TechnologyUpdate,
    TechnologyRemoved,

    # Measurements
    MeasurementUpdate,
    MeasurementRemoved,

    # MeteringPoints
    MeteringPointUpdate,
    MeteringPointRemoved,
    MeteringPointTechnologyUpdate,
    MeteringPointAddressUpdate,

)
