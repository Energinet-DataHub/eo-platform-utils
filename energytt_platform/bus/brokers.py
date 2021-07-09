from typing import List

from energytt.messages import Message


class MessageConsumer(object):
    def __iter__(self):
        raise NotImplementedError


class MessageBroker(object):
    def publish(self, topic: str, msg: Message, block=False):
        raise NotImplementedError

    def subscribe(self, topics: List[str]) -> MessageConsumer:
        raise NotImplementedError
