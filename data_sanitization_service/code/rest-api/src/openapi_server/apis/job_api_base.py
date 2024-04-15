# coding: utf-8

import json
import logging
import os
import uuid
from io import BytesIO

import kubernetes.client
import kubernetes.config
from fastapi import HTTPException
from jinja2 import Environment, FileSystemLoader
from kubernetes.client.rest import ApiException
from minio import Minio
from minio.error import MinioException
from typing import ClassVar, Dict, List, Tuple  # noqa: F401

from openapi_server.models.job import Job
from openapi_server.models.job_status import JobStatus
from openapi_server.models.submit_job200_response import SubmitJob200Response


logging.basicConfig(
    format='%(asctime)s %(levelname)-8s %(filename)s:%(lineno)s %(funcName)20s() %(message)s',
    level=logging.INFO,
    datefmt='%Y-%m-%d %H:%M:%S'
)

LOGGER = logging.getLogger(__name__)

CONFIG_KEY = {
    "columnScoringFunction": "column_score",
    "isFullyDistributed": "parallel",
    "input": "input",
    "idAttributes": "id_columns",
    "informationLossMeasures": "measures",
    "k": "K",
    "l": "L",
    "output": "output",
    "partitions": "fragments",
    "partitionFunction": "fragmentation",
    "quasiIdAttributes": "quasiid_columns",
    "redact": "redact",
    "samplingFraction": "fraction",
    "sensitiveAttributes": "sensitive_columns",
    "repartitionFunction": "repartition"
}

CONFIG_VALUES = {
    # column scoring functions
    "entropy": "entropy",
    "negativeEntropy": "neg_entropy",
    "normalizedSpan": "norm_span",
    "span": "span",
    # information loss measures
    "discernabilityPenalty": "discernability_penalty",
    "globalCertaintyPenalty": "global_certainty_penalty",
    "normalizedCertaintyPenalty": "normalized_certainty_penalty",
    # repartitioning function
    "byPartition": "customRepartition",
    "byRange": "repartitionByRange",
    "none": "noRepartition",
}

ENDPOINT = os.getenv("ENDPOINT", default="minio.minio-tenant.svc.cluster.local")
MINIO_CLIENT = Minio(
    ENDPOINT,
    access_key=os.getenv("AWS_ACCESS_KEY_ID", default="minio"),
    secret_key=os.getenv("AWS_SECRET_ACCESS_KEY", default="minio123")
)

ENV = Environment(loader=FileSystemLoader("templates"))
SPARK_APP_TEMPLATE = ENV.get_template("spark-app.json")

K8S_CLIENT_CONFIG = None
kubernetes.config.load_incluster_config(client_configuration=K8S_CLIENT_CONFIG)
K8S_CLIENT = kubernetes.client.ApiClient(K8S_CLIENT_CONFIG)
K8S_CUSTOM_CLIENT = kubernetes.client.CustomObjectsApi(K8S_CLIENT)


def delete_job(jobId: str) -> None:
    LOGGER.debug("jobId = %s", jobId)
    try:
        # Submit request for deletion to the K8s apiserver
        K8S_CUSTOM_CLIENT.delete_namespaced_custom_object(
            "sparkoperator.k8s.io",
            "v1beta2",
            "spark-app",
            "sparkapplications",
            f"data-sanitization-job-{jobId}",
            grace_period_seconds=None,
        )
        LOGGER.info("Deleted Spark application data-sanitization-job-%s", jobId)
    except ApiException:
        LOGGER.warning("Spark application data-sanitization-job-%s does not exist", jobId)


def get_job_status_by_id(jobId: str) -> JobStatus:
    LOGGER.debug("jobId = %s", jobId)
    jobStatus = JobStatus()
    try:
        # Submit request for status information to the K8s apiserver
        api_response = K8S_CUSTOM_CLIENT.get_namespaced_custom_object_status(
            "sparkoperator.k8s.io",
            "v1beta2",
            "spark-app",
            "sparkapplications",
            f"data-sanitization-job-{jobId}",
        )
        LOGGER.info("Got Spark application data-sanitization-job-%s status", jobId)

        jobStatus = api_response['status']['applicationState']
    except ApiException as error:
        LOGGER.error("Exception when getting Spark application "
                     "data-sanitization-job-%s: %s", jobId, error)
        if error.status == 404:
            raise HTTPException(status_code=404, detail="Job not found")
        raise HTTPException(status_code=500, detail="Error getting job status")

    return jobStatus


def submit_job(job: Job) -> SubmitJob200Response:
    LOGGER.debug("job = {%s}", job)
    req_id = str(uuid.uuid4())

    # Translate API config in the internal config
    job = job.to_dict()
    config = job.copy()
    # Remove Spark application parameters
    del config["driver"]
    del config["executor"]
    # Rename API values to Spark application values
    for api_key in ["columnScoringFunction", "repartitionFunction"]:
        if api_key in config:
            config[api_key] = CONFIG_VALUES[config[api_key]]
    api_key = "informationLossMeasures"
    if api_key in config:
        config[api_key] = [CONFIG_VALUES[api_value] for api_value in config[api_key]]
    # Rename API keys to Spark application keys
    config = {CONFIG_KEY[api_key]:value for api_key, value in config.items()}

    # Upload sanitization job config
    data = BytesIO(json.dumps(config).encode())
    try:
        result = MINIO_CLIENT.put_object(
            "sanitization",
            f"config/{req_id}.json",
            data,
            data.getbuffer().nbytes,
            content_type="application/json"
        )
        LOGGER.info("Created configuration %s with etag=%s and version-id=%s",
                    result.object_name, result.etag, result.version_id)
    except MinioException as error:
        LOGGER.error("Error creating sanitization job configuration: %s", error)
        raise HTTPException(
            status_code=500,
            detail="Error uploading job configuration"
        )

    # Customize the Spark application resource
    body = json.loads(
        SPARK_APP_TEMPLATE.render(
            req_id=req_id,
            endpoint=ENDPOINT,
            driver=job["driver"],
            executor=job["executor"],
        )
    )

    try:
        # Submit request for creation of the Spark application to the K8s
        # apiserver
        K8S_CUSTOM_CLIENT.create_namespaced_custom_object(
            "sparkoperator.k8s.io",
            "v1beta2",
            "spark-app",
            "sparkapplications",
            body,
            field_manager="data_sanitization_service"
        )
        LOGGER.info("Created Spark application data-sanitization-job-%s", req_id)
    except ApiException as error:
        LOGGER.error("Exception when creating Spark application "
                     "data-sanitization-job-%s: %s", req_id, error)
        raise HTTPException(
            status_code=500,
            detail="Error deploying job configuration"
        )

    return {"id": req_id}
