from energytt_platform.bus.registry import MessageRegistry

from .measurements import NewMeasurement, MeasurementUpdated


registry = MessageRegistry.from_message_types(
    NewMeasurement,
    MeasurementUpdated,
)
