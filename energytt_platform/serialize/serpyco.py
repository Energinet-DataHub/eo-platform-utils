from functools import lru_cache
from typing import Dict, Type, Any, Optional

from .serializer import Serializer, TSerializable

# TODO Describe why:
try:
    import serpyco
except ImportError:
    serpyco = None


@lru_cache
def _get_serpyco_serializer(cls: Type[TSerializable]) -> serpyco.Serializer:
    """
    TODO
    """
    return serpyco.Serializer(cls, strict=True)


class SerpycoSimpleSerializer(Serializer[Dict[str, Any]]):
    """
    Serialize and deserialize to and from simple Python types (dictionary).
    """
    def serialize(
            self, obj: TSerializable,
            cls: Optional[Type[TSerializable]] = None,
    ) -> Dict[str, Any]:
        """
        Serializes object to Python.
        """
        if cls is None:
            cls = obj.__class__
        return _get_serpyco_serializer(cls).dump(obj)

    def deserialize(
            self,
            data: Dict[str, Any],
            cls: Type[TSerializable],
    ) -> TSerializable:
        """
        Deserialize JSON data to instance of type "cls".
        """
        return _get_serpyco_serializer(cls).load(data)


class SerpycoJsonSerializer(Serializer[bytes]):
    """
    Serialize and deserialize to and from JSON (encoded bytes).
    """
    def serialize(
            self,
            obj: TSerializable,
            cls: Optional[Type[TSerializable]] = None,
    ) -> bytes:
        """
        Serializes object to JSON.
        """
        if cls is None:
            cls = obj.__class__
        return _get_serpyco_serializer(cls).dump_json(obj).encode()

    def deserialize(
            self,
            data: bytes,
            cls: Type[TSerializable],
    ) -> TSerializable:
        """
        Deserialize JSON data to instance of type "cls".
        """
        return _get_serpyco_serializer(cls).load_json(data.decode('utf8'))
