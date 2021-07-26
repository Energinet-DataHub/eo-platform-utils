from datetime import datetime, timedelta

from energytt_platform.bus import get_default_broker, topics
from energytt_platform.bus.messages import NewMeasurement
from energytt_platform.models.measurements import Measurement


broker = get_default_broker(['172.17.0.2:9092'])

broker.publish(
    topic=topics.MEASUREMENTS,
    msg=NewMeasurement(
        measurement=Measurement(
            gsrn='1234567890',
            amount=2000,
            begin=datetime.now(),
            end=datetime.now() + timedelta(days=1),
        ),
    ),
)
