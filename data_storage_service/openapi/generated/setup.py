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
    description="Data Storage Microservice",
    author_email="Guangyuan.Piao@dell.com",
    url="",
    keywords=["OpenAPI", "Data Storage Microservice"],
    install_requires=REQUIRES,
    packages=find_packages(),
    package_data={'': ['openapi/openapi.yaml']},
    include_package_data=True,
    entry_points={
        'console_scripts': ['openapi_server=openapi_server.__main__:main']},
    long_description="""\
    This is Data Storage Service (DSS) as part of the Novel Metadata Fabric based on the OpenAPI 3.1 specification.   It stores time series metrics and forecasting results such as daily energy consumption metrics and forecasting results from the prediction microservice and on the GLACIATION platform. It writes the most recent history and prediction of energy consumption of the platform to the Distributed Knowledge Graph (DKG). It allows to retrieve time series together with forecasting results.  It also stores data access patterns to keep track of data popularity in the platform, and write to DKG with daily statistics. It allows to retrieve daily summary statistics.  You can find out more about the DSS microservice at [https://github.com/glaciation-heu/IceStream/tree/development/data_storage_service](https://github.com/glaciation-heu/IceStream/tree/development/data_storage_service). 
    """
)

