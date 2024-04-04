import unittest

from flask import json

from openapi_server.models.data_access_record import DataAccessRecord  # noqa: E501
from openapi_server.models.metric import Metric  # noqa: E501
from openapi_server.test import BaseTestCase


class TestDefaultController(BaseTestCase):
    """DefaultController integration test stubs"""

    def test_add_data_access_record(self):
        """Test case for add_data_access_record

        Store data access record
        """
        data_access_record = {"dataId":"dataId","requestId":"requestId","time":"2000-01-23"}
        headers = { 
            'Accept': 'application/json',
            'Content-Type': 'application/json',
        }
        response = self.client.open(
            '/dataAccess',
            method='POST',
            headers=headers,
            data=json.dumps(data_access_record),
            content_type='application/json')
        self.assert200(response,
                       'Response body is : ' + response.data.decode('utf-8'))

    def test_add_prediction(self):
        """Test case for add_prediction

        Store prediction results
        """
        metric = {"forecasting_period":5,"forecasting_values":[6.0274563,6.0274563],"metricId":"metricId","timeseries":[0.8008282,0.8008282],"forecasting_model":"forecasting_model","time":["2000-01-23","2000-01-23"],"forecasting_upper_bounds":[1.4658129,1.4658129],"forecasting_lower_bounds":[5.962134,5.962134],"aggregation_interval":2}
        headers = { 
            'Accept': 'application/json',
            'Content-Type': 'application/json',
        }
        response = self.client.open(
            '/prediction',
            method='POST',
            headers=headers,
            data=json.dumps(metric),
            content_type='application/json')
        self.assert200(response,
                       'Response body is : ' + response.data.decode('utf-8'))

    def test_get_data_access_record(self):
        """Test case for get_data_access_record

        Get data access record for the given data dataId
        """
        query_string = [('start_time', '2024-02-28'),
                        ('end_time', '2024-08-28')]
        headers = { 
            'Accept': 'applicatin/json',
        }
        response = self.client.open(
            '/dataAccess/{data_id}'.format(data_id='data_id_example'),
            method='GET',
            headers=headers,
            query_string=query_string)
        self.assert200(response,
                       'Response body is : ' + response.data.decode('utf-8'))

    def test_get_metric(self):
        """Test case for get_metric

        Get prediction history for the given metricId and forecasting time
        """
        query_string = [('forecasting_time', '2024-02-28')]
        headers = { 
            'Accept': 'applicatin/json',
        }
        response = self.client.open(
            '/prediction/{metric_id}'.format(metric_id='metric_id_example'),
            method='GET',
            headers=headers,
            query_string=query_string)
        self.assert200(response,
                       'Response body is : ' + response.data.decode('utf-8'))

    def test_get_timeseries(self):
        """Test case for get_timeseries

        Get timeseries for the given metricId and forecasting time
        """
        query_string = [('start_time', '2024-02-28'),
                        ('end_time', '2024-08-28')]
        headers = { 
            'Accept': 'applicatin/json',
        }
        response = self.client.open(
            '/timeseries/{metric_id}'.format(metric_id='metric_id_example'),
            method='GET',
            headers=headers,
            query_string=query_string)
        self.assert200(response,
                       'Response body is : ' + response.data.decode('utf-8'))


if __name__ == '__main__':
    unittest.main()
