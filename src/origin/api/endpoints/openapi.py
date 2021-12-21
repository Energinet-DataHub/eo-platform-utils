from typing import Dict, Any

from ..endpoint import Endpoint
from ..openapi import generate_api_specs


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

    def handle_request(self) -> Dict[str, Any]:
        """
        :returns: Open API specifications as raw JSON
        """
        return generate_api_specs(self.app)
