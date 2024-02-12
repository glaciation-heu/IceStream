import connexion
from typing import Dict
from typing import Tuple
from typing import Union

from openapi_server.models.metric import Metric  # noqa: E501
from openapi_server import util
from openapi_server.prediction_service.utils import query

def get_metric_by_id(metric_id):  # noqa: E501
    """Retrieve historical and predicted time series by ID

    Returns a time series metric # noqa: E501

    :param metric_id: Id of the metric to return
    :type metric_id: int

    :rtype: Union[Metric, Tuple[Metric, int], Tuple[Metric, int, Dict[str, str]]
    """
    return query(metric_id)
