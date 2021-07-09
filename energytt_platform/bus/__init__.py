from .kafka import KafkaMessageBroker
from .serializers import ProtocolBuffersSerializer


def get_default_broker() -> KafkaMessageBroker:
    serializer = ProtocolBuffersSerializer()
    broker = KafkaMessageBroker(serializer)
    return broker
