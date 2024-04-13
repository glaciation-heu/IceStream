# coding: utf-8

from typing import Dict, List  # noqa: F401
import importlib
import pkgutil

from openapi_server.apis.job_api_base import delete_job as delete_job_impl
from openapi_server.apis.job_api_base import get_job_status_by_id as get_job_status_by_id_impl
from openapi_server.apis.job_api_base import submit_job as submit_job_impl
import openapi_server.impl

from fastapi import (  # noqa: F401
    APIRouter,
    Body,
    Cookie,
    Depends,
    Form,
    Header,
    Path,
    Query,
    Response,
    Security,
    status,
)

from openapi_server.models.extra_models import TokenModel  # noqa: F401
from openapi_server.models.job import Job
from openapi_server.models.job_status import JobStatus
from openapi_server.models.k_anonymity_job import KAnonymityJob
from openapi_server.models.l_diversity_job import LDiversityJob
from openapi_server.models.submit_job200_response import SubmitJob200Response


router = APIRouter()

ns_pkg = openapi_server.impl
for _, name, _ in pkgutil.iter_modules(ns_pkg.__path__, ns_pkg.__name__ + "."):
    importlib.import_module(name)


@router.delete(
    "/api/v1alpha1/job/{jobId}",
    responses={
        200: {"description": "Successful deletion of the data sanitization job"},
        400: {"description": "Invalid job ID"},
    },
    tags=["job"],
    summary="Delete data sanitization job by ID",
    response_model_by_alias=True,
)
async def delete_job(
    jobId: str = Path(..., description=""),
) -> None:
    return delete_job_impl(jobId)


@router.get(
    "/api/v1alpha1/job/{jobId}/status",
    responses={
        200: {"model": JobStatus, "description": "Successful retrieval of the data sanitization job status"},
        400: {"description": "Invalid job ID"},
        404: {"description": "Job not found"},
    },
    tags=["job"],
    summary="Get status of data sanitization job by ID",
    response_model_by_alias=True,
)
async def get_job_status_by_id(
    jobId: str = Path(..., description=""),
) -> JobStatus:
    return get_job_status_by_id_impl(jobId)


@router.post(
    "/api/v1alpha1/job",
    responses={
        200: {"model": SubmitJob200Response, "description": "Successful creation of the data sanitization job"},
        400: {"description": "Invalid job syntax"},
        422: {"description": "Invalid job declaration"},
    },
    tags=["job"],
    summary="Create a data sanitization job",
    response_model_by_alias=True,
)
async def submit_job(
    job: Job = Body(None, description=""),
) -> SubmitJob200Response:
    return submit_job_impl(job)
