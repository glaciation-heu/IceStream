# coding: utf-8

from fastapi.testclient import TestClient


from openapi_server.models.job import Job  # noqa: F401
from openapi_server.models.job_status import JobStatus  # noqa: F401
from openapi_server.models.submit_job200_response import SubmitJob200Response  # noqa: F401


def test_delete_job(client: TestClient):
    """Test case for delete_job

    Delete data sanitization job by ID
    """

    headers = {
    }
    # uncomment below to make a request
    #response = client.request(
    #    "DELETE",
    #    "/api/v1alpha1/job/{jobId}".format(jobId='job_id_example'),
    #    headers=headers,
    #)

    # uncomment below to assert the status code of the HTTP response
    #assert response.status_code == 200


def test_get_job_status_by_id(client: TestClient):
    """Test case for get_job_status_by_id

    Get status of data sanitization job by ID
    """

    headers = {
    }
    # uncomment below to make a request
    #response = client.request(
    #    "GET",
    #    "/api/v1alpha1/job/{jobId}/status".format(jobId='job_id_example'),
    #    headers=headers,
    #)

    # uncomment below to assert the status code of the HTTP response
    #assert response.status_code == 200


def test_submit_job(client: TestClient):
    """Test case for submit_job

    Create a data sanitization job
    """
    job = {"id_attributes":["exampleIdAttribute"],"partitions":4,"quasi_id_attributes":["exampleQuasiIdAttribute0","exampleQuasiIdAttribute1"],"sampling_fraction":0.08008281904610115,"repartition_function":"byRange","redact":0,"k":100,"output":"hdfs://namenode:8020/anonymized/adults.csv","input":"hdfs://namenode:8020/dataset/adults.csv","column_scoring_function":"span","is_fully_distributed":1,"information_loss_measures":["discernabilityPenalty","globalCertaintyPenalty","normalizedCertaintyPenalty"],"driver":{"memory":"512m"},"executor":{"memory":"512m","instances":4},"partition_function":"mondrian"}

    headers = {
    }
    # uncomment below to make a request
    #response = client.request(
    #    "POST",
    #    "/api/v1alpha1/job",
    #    headers=headers,
    #    json=job,
    #)

    # uncomment below to assert the status code of the HTTP response
    #assert response.status_code == 200

