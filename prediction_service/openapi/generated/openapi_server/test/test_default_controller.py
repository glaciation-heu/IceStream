import unittest

from flask import json

from openapi_server.models.metric import Metric  # noqa: E501
from openapi_server.test import BaseTestCase


class TestDefaultController(BaseTestCase):
    """DefaultController integration test stubs"""

    def test_get_metric_by_id(self):
        """Test case for get_metric_by_id

        Retrieve historical and predicted time series by ID
        """
        headers = { 
            'Accept': 'applicatin/json',
        }
        response = self.client.open(
            '/prediction/{metric_id}'.format(metric_id=56),
            method='GET',
            headers=headers)
        self.assert200(response,
                       'Response body is : ' + response.data.decode('utf-8'))


if __name__ == '__main__':
    unittest.main()
