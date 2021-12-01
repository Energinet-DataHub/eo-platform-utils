import json
from typing import List
from dataclasses import dataclass
from openapi_specgen import OpenApi, OpenApiParam, OpenApiPath, OpenApiResponse


@dataclass
class Hello:
    foobar: str


@dataclass
class World:
    name: str
    age: int
    asd: Hello


sample_response = OpenApiResponse('Response description', data_type=World)
sample_param = OpenApiParam('param_name', 'query', data_type=str)
sample_path = OpenApiPath('/api_path', 'get', [sample_response], [sample_param])

# marshmallow_response = OpenApiResponse('Response description', data_type=MarshmallowSchema)
# marshmallow_path = OpenApiPath('/api_path', 'post', [sample_response], requestBody=MarshmallowSchema)

sample_api = OpenApi('Sample Api', [sample_path])

print(json.dumps(sample_api.as_dict(), indent=4))
k = 2
