from serpyco import field
from datetime import datetime
from dataclasses import dataclass
from typing import Generic, TypeVar, Union, Dict, Any, Optional

from origin.serialize import json_serializer, simple_serializer

from .broker import Message
from .registry import MessageRegistry


TWrappedMessage = TypeVar('TWrappedMessage', bound=Message)
TSerializedMessage = Dict[str, Any]


@dataclass
class WrappedMessage(Message, Generic[TWrappedMessage]):
    """Dataclass to wrap messages."""

    type: str
    time: datetime = field(default_factory=datetime.now)
    msg: Optional[Union[TWrappedMessage, TSerializedMessage]] = \
        field(default=None)


class MessageSerializer(object):
    """
    A serializer for serializing messages.

    A serializer specifically for serializing messages to and from the
    event bus.
    """

    class SerializeError(Exception):
        """Serialization error."""

        pass

    class DeserializeError(Exception):
        """Deserialization error."""

        pass

    def __init__(self, registry: MessageRegistry):
        self.registry = registry

    def serialize(self, msg: Message) -> bytes:
        """Wrap a message appropriately and JSON serializes it."""

        if msg not in self.registry:
            raise self.SerializeError((
                f'Can not serialize of type "{msg.__class__.__name__}": '
                'Type is unknown to the bus.'
            ))

        wrapped_msg = WrappedMessage(
            type=msg.__class__.__name__,
            msg=msg,
        )

        return json_serializer.serialize(
            obj=wrapped_msg,
            schema=WrappedMessage[msg.__class__],
        )

    def deserialize(self, data: bytes) -> Message:
        """Deserializes JSON bytestream into a message."""

        wrapped_msg = json_serializer.deserialize(
            data=data,
            schema=WrappedMessage[TSerializedMessage],
        )

        if wrapped_msg.type not in self.registry:
            raise self.DeserializeError((
                f'Can not deserialize message of type "{wrapped_msg.type}": '
                'Type is unknown to the bus.'
            ))

        message_cls = self.registry.get(wrapped_msg.type)

        return simple_serializer.deserialize(
            data=wrapped_msg.msg,
            schema=message_cls,
        )
