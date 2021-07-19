from typing import Union, Type

from energytt_platform.serialize import Serializable


class MessageRegistry(dict):
    """
    A registry of all messages that the bus knows of.

    Works a a dict where:
        Key = Message type name (str)
        Value = Message class (Serializable)

    TODO Enforce unique names
    """

    @classmethod
    def from_message_types(cls, *message_types: Type[Serializable]) -> 'MessageRegistry':
        return cls({c.__name__: c for c in message_types})

    def __contains__(self, item: Union[str, Serializable, Type[Serializable]]) -> bool:
        if isinstance(item, str):
            return item in self.keys()
        elif issubclass(item, Serializable):
            return item in self.values()
        elif isinstance(item, Serializable):
            return item.__class__ in self.values()
        else:
            return False
