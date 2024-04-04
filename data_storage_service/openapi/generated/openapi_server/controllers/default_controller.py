import connexion
from typing import Dict
from typing import Tuple
from typing import Union

from openapi_server.models.data_access_record import DataAccessRecord  # noqa: E501
from openapi_server.models.metric import Metric  # noqa: E501
from openapi_server import util
from openapi_server.data_storage_service import utils


def add_data_access_record(data_access_record=None):  # noqa: E501
    """Store data access record

    Store data access record to database # noqa: E501

    :param data_access_record: Store data access record to database
    :type data_access_record: dict | bytes

    :rtype: 
    """
    if connexion.request.is_json:
        data_access_record = DataAccessRecord.from_dict(connexion.request.get_json())  # noqa: E501
    return utils.writeDataAccessRecord(data_access_record)


def add_prediction(metric=None):  # noqa: E501
    """Store prediction results

    Store prediction results to database # noqa: E501

    :param metric: Store prediction results to database
    :type metric: dict | bytes

    :rtype: Union[Metric, Tuple[Metric, int], Tuple[Metric, int, Dict[str, str]]
    """
    if connexion.request.is_json:
        metric = Metric.from_dict(connexion.request.get_json())  # noqa: E501
    return utils.writePredictionResults(metric)


def get_data_access_record(data_id, start_time=None, end_time=None):  # noqa: E501
    """Get data access record for the given data dataId

    Get data access record for the given data dataId # noqa: E501

    :param data_id: Data source Id
    :type data_id: str
    :param start_time: Filtering start time of data access records
    :type start_time: str
    :param end_time: Filtering end time of data access records
    :type end_time: str

    :rtype: Union[List[DataAccessRecord], Tuple[List[DataAccessRecord], int], Tuple[List[DataAccessRecord], int, Dict[str, str]]
    """
    start_time = util.deserialize_datetime(start_time)
    end_time = util.deserialize_datetime(end_time)

    return utils.readDataAccessRecord(data_id, start_time, end_time)


def get_metric(forecasting_time, metric_id):  # noqa: E501
    """Get prediction history for the given metricId and forecasting time

    Returns Metric # noqa: E501

    :param forecasting_time: Time of the forecasting
    :type forecasting_time: str
    :param metric_id: Id of the metric to return
    :type metric_id: str

    :rtype: 
    """
    forecasting_time = util.deserialize_date(forecasting_time)
    print(forecasting_time, metric_id)
    return utils.readPredictionResults(metric_id, forecasting_time)


def get_timeseries(metric_id, start_time=None, end_time=None):  # noqa: E501
    """Get timeseries for the given metricId and forecasting time

    Returns TimeSeries # noqa: E501

    :param metric_id: Id of the metric to return
    :type metric_id: str
    :param start_time: Filtering start time of timeseries
    :type start_time: str
    :param end_time: Filtering end time of timeseries
    :type end_time: str

    :rtype:
    """
    start_time = util.deserialize_date(start_time)
    end_time = util.deserialize_date(end_time)
    return utils.readTimeseries(metric_id, start_time, end_time)
