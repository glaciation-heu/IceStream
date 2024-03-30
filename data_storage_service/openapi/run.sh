#!/bin/bash
# Generate code using OpenAPI specification - openapi.yaml
openapi-generator-cli generate -i openapi.yaml -o generated -g python-flask --skip-operation-example
# Fix requirements.txt
sed -i '1 s/connexion\[swagger-ui\]/connexion\[swagger-ui,flask\]/' generated/requirements.txt  && sed -i '$ s/Flask/\#Flask/' generated/requirements.txt
echo "influxdb-client == 1.40.0" >> generated/requirements.txt
# Fix encoder.py
sed -i 's/connexion.apps.flask_app/json/' generated/openapi_server/encoder.py && sed -i 's/FlaskJSONEncoder/JSONEncoder/' generated/openapi_server/encoder.py
# Fix openapi version in the specification
sed -i '1 s/3.1.0/3.0.0/' generated/openapi_server/openapi/openapi.yaml
# Run the openapi server
cd generated
python -m openapi_server
