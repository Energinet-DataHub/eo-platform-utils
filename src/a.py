from dataclasses import dataclass
from pprint import pprint

from dataclasses_jsonschema import JsonSchemaMixin


@dataclass
class Asd(JsonSchemaMixin):
    "A 2D point"
    z: float


@dataclass
class Point(JsonSchemaMixin):
    "A 2D point"
    x: float
    y: float
    asd: Asd


pprint(Point.json_schema())
