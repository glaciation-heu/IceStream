import sys
from setuptools import setup, find_packages

NAME = "openapi_server"
VERSION = "1.0.0"

# To install the library, run the following
#
# python setup.py install
#
# prerequisite: setuptools
# http://pypi.python.org/pypi/setuptools

REQUIRES = [
    "connexion>=2.0.2",
    "swagger-ui-bundle>=0.0.2",
    "python_dateutil>=2.6.0"
]

setup(
    name=NAME,
    version=VERSION,
    description="Prediction Microservice",
    author_email="Guangyuan.Piao@dell.com",
    url="",
    keywords=["OpenAPI", "Prediction Microservice"],
    install_requires=REQUIRES,
    packages=find_packages(),
    package_data={'': ['openapi/openapi.yaml']},
    include_package_data=True,
    entry_points={
        'console_scripts': ['openapi_server=openapi_server.__main__:main']},
    long_description="""\
    This is prediction microservice as part of the Novel Metadata Fabric based on the OpenAPI 3.1 specification. It provides a forecasting functionality for pre-defined metrics such as daily energy consumption metrics on the GLACIATION platform. You can retrieve the most recent history and prediction of energy consumption of the platform.  You can find out more about the prediction microservice at [https://github.com/glaciation-heu/IceStream/tree/development/prediction_service](https://github.com/glaciation-heu/IceStream/tree/development/prediction_service). 
    """
)

