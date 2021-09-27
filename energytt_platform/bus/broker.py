from abc import abstractmethod
from dataclasses import dataclass
from typing import List, Iterable, Callable, Any, Optional, Union, Tuple

from energytt_platform.serialize import Serializable


@dataclass
class Message(Serializable):
    """
    Base-class for messages that can be sent on the bus.
    Inherited classes must remember to use the @dataclass decorator.
    """
    pass


TTopic = str
TTopicList = Union[List[TTopic], Tuple[TTopic, ...]]

TMessageHandler = Callable[[Message], None]


class MessageBroker(object):
    """
    Abstract base-class for publishing and consuming messages
    on the message-bus.
    """

    class PublishError(Exception):
        """
        TODO
        """
        pass

    class DispatchError(Exception):
        """
        TODO
        """
        pass

    @abstractmethod
    def publish(self, topic: TTopic, msg: Any, block=False, timeout=10):
        """
        Publish a message to a topic on the bus.

        :param topic: The topic to publish to
        :param msg: The message to publish
        :param block: Whether to block until publishing is complete
        :param timeout: Timeout in seconds (if block=True)
        """
        raise NotImplementedError

    @abstractmethod
    def subscribe(self, topics: TTopicList):
        """
        Invoked the handler for incoming messages in any of the topics.

        :param topics: The topics to subscribe to
        """
        raise NotImplementedError

    @abstractmethod
    def listen(self) -> Iterable[Message]:
        """
        Returns an iterable of messages received in any
        of the subscribed topics.
        """
        raise NotImplementedError

    # def listen222(self, topics: List[str], handler: TMessageHandler):
    #     """
    #     An alias for subscribe() except this function takes a callable
    #     which is invoked for each message.
    #
    #     :param topics: The topics to subscribe to
    #     :param handler: Message handler
    #     """
    #     for msg in self.subscribe(topics):
    #         handler(msg)

    # def subscribe2222(self, topics: List[str], handler: TMessageHandler):
    #     """
    #     An alias for subscribe() except this function takes a callable
    #     which is invoked for each message.
    #
    #     :param topics: The topics to subscribe to
    #     :param handler: Message handler
    #     """
    #     for msg in self.subscribe(topics):
    #         handler(msg)

    # @abstractmethod
    # def subscribe_listen(
    #         self,
    #         topics: List[str],
    #         handler: Optional[TMessageHandler],
    # ) -> Iterable[Message]:
    #     """
    #     Invoked the handler for incoming messages in any of the topics.
    #
    #     :param topics: The topics to subscribe to
    #     :param handler: Message handler
    #     """
    #     raise NotImplementedError
