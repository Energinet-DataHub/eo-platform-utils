import json
import dataclasses
from google.protobuf.any_pb2 import Any

from energytt.messages import Message


__message_serializers = {}


class MessageSerializer(object):
    def serialize(self, message: Message) -> bytes:
        raise NotImplementedError

    def deserialize(self, data: bytes) -> Message:
        raise NotImplementedError


class JsonSerializer(MessageSerializer):
    def serialize(self, msg: Message) -> bytes:
        return json.dumps(dataclasses.asdict(msg)).encode()

    def deserialize(self, data: bytes) -> Message:
        return json.loads(data.decode('utf8'))


class ProtocolBuffersSerializer(MessageSerializer):
    def serialize(self, msg: Message) -> bytes:
        x = Any()
        x.Pack(msg)
        return x.SerializeToString().encode()

    def deserialize(self, data: bytes) -> Message:
        return json.loads(data.decode('utf8'))
