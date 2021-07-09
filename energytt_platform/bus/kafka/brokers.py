from typing import List
from kafka import KafkaProducer, KafkaConsumer
from kafka.errors import KafkaError

from energytt.messages import Message

from ..exceptions import PublishError
from ..serializers import MessageSerializer
from ..brokers import MessageConsumer, MessageBroker


class KafkaMessageConsumer(MessageConsumer):
    def __init__(self, topics: List[str], serializer: MessageSerializer):
        self.topics = topics
        self.serializer = serializer

    def __iter__(self):
        consumer = KafkaConsumer(*self.topics,
                                 # group_id='my-group',
                                 bootstrap_servers=['172.17.0.2:9092'],
                                 value_deserializer=self.serializer.deserialize,
                                 auto_offset_reset='earliest', enable_auto_commit=False)

        return (msg.value for msg in consumer)


class KafkaMessageBroker(MessageBroker):
    def __init__(self, serializer: MessageSerializer):
        self.serializer = serializer

    def publish(self, topic: str, msg: Message, block=False, timeout=10):
        producer = KafkaProducer(bootstrap_servers=['172.17.0.2:9092'])
        future = producer.send(topic, self.serializer.serialize(msg))

        # Block for 'synchronous' sends
        try:
            record_metadata = future.get(timeout=timeout)
        except KafkaError as e:
            # Decide what to do if produce request failed...
            raise PublishError(str(e))

    def subscribe(self, topics: List[str]) -> KafkaMessageConsumer:
        return KafkaMessageConsumer(
            topics=topics,
            serializer=self.serializer,
        )
