from .serializer import Serializer, Serializable
from .serpyco import SerpycoSimpleSerializer, SerpycoJsonSerializer


json_serializer = SerpycoSimpleSerializer()

simple_serializer = SerpycoJsonSerializer()
