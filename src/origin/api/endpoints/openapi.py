from openapi_specgen import (
    OpenApi,
    OpenApiParam,
    OpenApiPath,
    OpenApiResponse,
)

from ..endpoint import Endpoint


SWAGGER_HTML = """
    <!DOCTYPE html>
    <html lang="en">
      <head>
        <meta charset="UTF-8">
        <title>Swagger UI</title>
        <link rel="stylesheet" type="text/css" href="https://unpkg.com/swagger-ui-dist@3.52.5/swagger-ui.css" />
      </head>
    
      <body>
        <div id="swagger-ui"></div>
    
        <script src="https://unpkg.com/swagger-ui-dist@3/swagger-ui-bundle.js" charset="UTF-8"> </script>
        <script src="https://unpkg.com/swagger-ui-dist@3.52.5/swagger-ui-standalone-preset.js" charset="UTF-8"> </script>
        <script>
            window.onload = function() {
              // Begin Swagger UI call region
              const ui = SwaggerUIBundle({
                url: "%(openapi_json_url)s",
                dom_id: '#swagger-ui',
                deepLinking: true,
                presets: [
                  SwaggerUIBundle.presets.apis,
                  SwaggerUIStandalonePreset
                ],
                plugins: [
                  SwaggerUIBundle.plugins.DownloadUrl
                ],
                layout: "StandaloneLayout"
              });
              // End Swagger UI call region
        
              window.ui = ui;
            };
          </script>
      </body>
    </html>
"""


class OpenApiSwaggerUI(Endpoint):
    """
    TODO
    """
    def __init__(self, specs_url: str):
        """
        :param specs_url: Absolute URL to raw OpenApi specs endpoint
        """
        self.specs_url = specs_url

    def handle_request(self) -> str:
        return SWAGGER_HTML % {
            'openapi_json_url': self.specs_url,
        }


class OpenApiSpecs(Endpoint):
    """
    TODO
    """
    def __init__(self, app: 'Application'):
        """
        :param app: Application object
        """
        self.app = app

    def handle_request(self):
        paths = []

        for e in self.app.endpoints:
            response = OpenApiResponse(
                descr='Response description',
                data_type=e.endpoint.Response,
            )

            path = OpenApiPath(
                path=e.path,
                method=e.method,
                responses=[response],
                params=[sample_param],
            )

            paths.append(path)

        sample_response = OpenApiResponse('Response description', data_type=World)
        sample_param = OpenApiParam('param_name', 'query', data_type=str)
        sample_path = OpenApiPath('/api_path', 'get', [sample_response], [sample_param])

        sample_api = OpenApi('Sample Api', [paths])

        return sample_api.as_dict()

        return {
            "openapi": "3.0.2",
            "info": {
                "title": "Sample Api",
                "version": "3.0.2"
            },
            "paths": {
                "/api_path": {
                    "get": {
                        "description": "",
                        "summary": "",
                        "operationId": "[get]_/api_path",
                        "responses": {
                            "200": {
                                "description": "Response description",
                                "content": {
                                    "application/json": {
                                        "schema": {
                                            "$ref": "#/components/schemas/World"
                                        }
                                    }
                                }
                            }
                        },
                        "parameters": [
                            {
                                "required": True,
                                "name": "param_name",
                                "in": "query",
                                "schema": {
                                    "type": "string",
                                    "title": "Param_Name"
                                }
                            }
                        ]
                    }
                }
            },
            "components": {
                "schemas": {
                    "World": {
                        "title": "World",
                        "required": [
                            "name",
                            "age",
                            "asd"
                        ],
                        "type": "object",
                        "properties": {
                            "name": {
                                "type": "string"
                            },
                            "age": {
                                "type": "integer"
                            },
                            "asd": {
                                "$ref": "#/components/schemas/Hello"
                            }
                        }
                    },
                    "Hello": {
                        "title": "Hello",
                        "required": [
                            "foobar"
                        ],
                        "type": "object",
                        "properties": {
                            "foobar": {
                                "type": "string"
                            }
                        }
                    }
                }
            }
        }
