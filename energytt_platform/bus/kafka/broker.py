from typing import List, Any, Iterable
from functools import cached_property
from kafka import KafkaProducer, KafkaConsumer, ConsumerRebalanceListener

from energytt_platform.bus.broker import MessageBroker, Message, TTopicList, TMessageHandler
from energytt_platform.bus.serialize import MessageSerializer


class KafkaMessageBroker(MessageBroker):
    """
    Implementation of Kafka as message bus.
    """
    def __init__(
            self,
            group: str,
            servers: List[str],
            serializer: MessageSerializer,
    ):
        self.group = group
        self.servers = servers
        self.serializer = serializer

    @cached_property
    def _kafka_producer(self) -> KafkaProducer:
        """
        TODO
        """
        return KafkaProducer(
            bootstrap_servers=self.servers,
            value_serializer=self.serializer.serialize,

        )

    @cached_property
    def _kafka_consumer(self) -> KafkaConsumer:
        """
        TODO
        """
        return KafkaConsumer(
            bootstrap_servers=self.servers,
            value_deserializer=self.serializer.deserialize,
            group_id=self.group,
            auto_offset_reset='latest',
            enable_auto_commit=False,
        )

    def publish(self, topic: str, msg: Any, block=True, timeout=10):
        """
        TODO
        """
        print('PUBLISH: %s' % msg)
        self._kafka_producer.send(topic=topic, value=msg)
        self._kafka_producer.flush()

        # future = self._kafka_producer.send(
        #     topic=topic,
        #     value=msg,
        # )
        #
        # if block:
        #     try:
        #         record_metadata = future.get(timeout=timeout)
        #     except KafkaError as e:
        #         # Decide what to do if produce request failed...
        #         raise self.PublishError(str(e))

    def subscribe(self, topics: TTopicList):
        """
        Invoked the handler for incoming messages in any of the topics.

        :param topics: The topics to subscribe to
        """
        self._kafka_consumer.subscribe(topics)

    def listen(self, topics) -> Iterable[Message]:
        """
        Returns an iterable of messages received in any
        of the subscribed topics.
        """
        kafka_consumer = KafkaConsumer(
            *topics,
            bootstrap_servers=self.servers,
            value_deserializer=self.serializer.deserialize,
            group_id=self.group,
            auto_offset_reset='latest',
            enable_auto_commit=False,
        )

        return (msg.value for msg in kafka_consumer)

    # def subscribe(self, topics: List[str]) -> Iterable[Message]:
    #     """
    #     TODO
    #     """
    #     kafka_consumer = KafkaConsumer(
    #         *topics,
    #         bootstrap_servers=self.servers,
    #         value_deserializer=self.serializer.deserialize,
    #         group_id=self.group,
    #         auto_offset_reset='latest',
    #         enable_auto_commit=False,
    #     )
    #
    #     kafka_consumer.subscribe()
    #
    #     return (msg.value for msg in self._kafka_consumer)
