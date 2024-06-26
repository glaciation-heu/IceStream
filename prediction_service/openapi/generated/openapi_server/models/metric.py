from datetime import date, datetime  # noqa: F401

from typing import List, Dict  # noqa: F401

from openapi_server.models.base_model import Model
from openapi_server import util


class Metric(Model):
    """NOTE: This class is auto generated by OpenAPI Generator (https://openapi-generator.tech).

    Do not edit the class manually.
    """

    def __init__(self, metric_id=None, timeseries=None, forecasting_values=None, forecasting_upper_bounds=None, forecasting_lower_bounds=None, forecasting_model=None, forecasting_period=None, time=None, aggregation_interval=None):  # noqa: E501
        """Metric - a model defined in OpenAPI

        :param metric_id: The metric_id of this Metric.  # noqa: E501
        :type metric_id: str
        :param timeseries: The timeseries of this Metric.  # noqa: E501
        :type timeseries: List[float]
        :param forecasting_values: The forecasting_values of this Metric.  # noqa: E501
        :type forecasting_values: List[float]
        :param forecasting_upper_bounds: The forecasting_upper_bounds of this Metric.  # noqa: E501
        :type forecasting_upper_bounds: List[float]
        :param forecasting_lower_bounds: The forecasting_lower_bounds of this Metric.  # noqa: E501
        :type forecasting_lower_bounds: List[float]
        :param forecasting_model: The forecasting_model of this Metric.  # noqa: E501
        :type forecasting_model: str
        :param forecasting_period: The forecasting_period of this Metric.  # noqa: E501
        :type forecasting_period: int
        :param time: The time of this Metric.  # noqa: E501
        :type time: List[date]
        :param aggregation_interval: The aggregation_interval of this Metric.  # noqa: E501
        :type aggregation_interval: int
        """
        self.openapi_types = {
            'metric_id': str,
            'timeseries': List[float],
            'forecasting_values': List[float],
            'forecasting_upper_bounds': List[float],
            'forecasting_lower_bounds': List[float],
            'forecasting_model': str,
            'forecasting_period': int,
            'time': List[date],
            'aggregation_interval': int
        }

        self.attribute_map = {
            'metric_id': 'metricId',
            'timeseries': 'timeseries',
            'forecasting_values': 'forecasting_values',
            'forecasting_upper_bounds': 'forecasting_upper_bounds',
            'forecasting_lower_bounds': 'forecasting_lower_bounds',
            'forecasting_model': 'forecasting_model',
            'forecasting_period': 'forecasting_period',
            'time': 'time',
            'aggregation_interval': 'aggregation_interval'
        }

        self._metric_id = metric_id
        self._timeseries = timeseries
        self._forecasting_values = forecasting_values
        self._forecasting_upper_bounds = forecasting_upper_bounds
        self._forecasting_lower_bounds = forecasting_lower_bounds
        self._forecasting_model = forecasting_model
        self._forecasting_period = forecasting_period
        self._time = time
        self._aggregation_interval = aggregation_interval

    @classmethod
    def from_dict(cls, dikt) -> 'Metric':
        """Returns the dict as a model

        :param dikt: A dict.
        :type: dict
        :return: The Metric of this Metric.  # noqa: E501
        :rtype: Metric
        """
        return util.deserialize_model(dikt, cls)

    @property
    def metric_id(self) -> str:
        """Gets the metric_id of this Metric.


        :return: The metric_id of this Metric.
        :rtype: str
        """
        return self._metric_id

    @metric_id.setter
    def metric_id(self, metric_id: str):
        """Sets the metric_id of this Metric.


        :param metric_id: The metric_id of this Metric.
        :type metric_id: str
        """

        self._metric_id = metric_id

    @property
    def timeseries(self) -> List[float]:
        """Gets the timeseries of this Metric.


        :return: The timeseries of this Metric.
        :rtype: List[float]
        """
        return self._timeseries

    @timeseries.setter
    def timeseries(self, timeseries: List[float]):
        """Sets the timeseries of this Metric.


        :param timeseries: The timeseries of this Metric.
        :type timeseries: List[float]
        """

        self._timeseries = timeseries

    @property
    def forecasting_values(self) -> List[float]:
        """Gets the forecasting_values of this Metric.


        :return: The forecasting_values of this Metric.
        :rtype: List[float]
        """
        return self._forecasting_values

    @forecasting_values.setter
    def forecasting_values(self, forecasting_values: List[float]):
        """Sets the forecasting_values of this Metric.


        :param forecasting_values: The forecasting_values of this Metric.
        :type forecasting_values: List[float]
        """

        self._forecasting_values = forecasting_values

    @property
    def forecasting_upper_bounds(self) -> List[float]:
        """Gets the forecasting_upper_bounds of this Metric.


        :return: The forecasting_upper_bounds of this Metric.
        :rtype: List[float]
        """
        return self._forecasting_upper_bounds

    @forecasting_upper_bounds.setter
    def forecasting_upper_bounds(self, forecasting_upper_bounds: List[float]):
        """Sets the forecasting_upper_bounds of this Metric.


        :param forecasting_upper_bounds: The forecasting_upper_bounds of this Metric.
        :type forecasting_upper_bounds: List[float]
        """

        self._forecasting_upper_bounds = forecasting_upper_bounds

    @property
    def forecasting_lower_bounds(self) -> List[float]:
        """Gets the forecasting_lower_bounds of this Metric.


        :return: The forecasting_lower_bounds of this Metric.
        :rtype: List[float]
        """
        return self._forecasting_lower_bounds

    @forecasting_lower_bounds.setter
    def forecasting_lower_bounds(self, forecasting_lower_bounds: List[float]):
        """Sets the forecasting_lower_bounds of this Metric.


        :param forecasting_lower_bounds: The forecasting_lower_bounds of this Metric.
        :type forecasting_lower_bounds: List[float]
        """

        self._forecasting_lower_bounds = forecasting_lower_bounds

    @property
    def forecasting_model(self) -> str:
        """Gets the forecasting_model of this Metric.


        :return: The forecasting_model of this Metric.
        :rtype: str
        """
        return self._forecasting_model

    @forecasting_model.setter
    def forecasting_model(self, forecasting_model: str):
        """Sets the forecasting_model of this Metric.


        :param forecasting_model: The forecasting_model of this Metric.
        :type forecasting_model: str
        """

        self._forecasting_model = forecasting_model

    @property
    def forecasting_period(self) -> int:
        """Gets the forecasting_period of this Metric.


        :return: The forecasting_period of this Metric.
        :rtype: int
        """
        return self._forecasting_period

    @forecasting_period.setter
    def forecasting_period(self, forecasting_period: int):
        """Sets the forecasting_period of this Metric.


        :param forecasting_period: The forecasting_period of this Metric.
        :type forecasting_period: int
        """

        self._forecasting_period = forecasting_period

    @property
    def time(self) -> List[date]:
        """Gets the time of this Metric.


        :return: The time of this Metric.
        :rtype: List[date]
        """
        return self._time

    @time.setter
    def time(self, time: List[date]):
        """Sets the time of this Metric.


        :param time: The time of this Metric.
        :type time: List[date]
        """

        self._time = time

    @property
    def aggregation_interval(self) -> int:
        """Gets the aggregation_interval of this Metric.


        :return: The aggregation_interval of this Metric.
        :rtype: int
        """
        return self._aggregation_interval

    @aggregation_interval.setter
    def aggregation_interval(self, aggregation_interval: int):
        """Sets the aggregation_interval of this Metric.


        :param aggregation_interval: The aggregation_interval of this Metric.
        :type aggregation_interval: int
        """

        self._aggregation_interval = aggregation_interval
