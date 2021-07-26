from typing import Any

from energytt_platform.bus import get_default_broker, topics


def on_measurements_topic(msg: Any):
    """
    A message was received.
    """
    print(msg)


broker = get_default_broker(['172.17.0.2:9092'])
broker.subscribe(
    topics=[topics.MEASUREMENTS],
    handler=on_measurements_topic,
)
