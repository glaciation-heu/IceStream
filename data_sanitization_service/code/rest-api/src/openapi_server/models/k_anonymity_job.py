# coding: utf-8

"""
    Data Sanitization Service

    This service implements an efficient and effective approach to protect users data by obfuscating information that can disclose their identities and sensitive information.

    The version of the OpenAPI document: 0.1.0
    Contact: seclab@unibg.it
    Generated by OpenAPI Generator (https://openapi-generator.tech)

    Do not edit the class manually.
"""  # noqa: E501


from __future__ import annotations
import pprint
import re  # noqa: F401
import json




from pydantic import BaseModel, ConfigDict, Field, StrictBool, StrictStr, field_validator
from typing import Any, ClassVar, Dict, List, Optional, Union
from typing_extensions import Annotated
from openapi_server.models.common_job_executor import CommonJobExecutor
from openapi_server.models.spark_pod_spec import SparkPodSpec
try:
    from typing import Self
except ImportError:
    from typing_extensions import Self

class KAnonymityJob(BaseModel):
    """
    Configuration of the k-anonymity data sanitization job
    """ # noqa: E501
    column_scoring_function: Optional[StrictStr] = Field(default='span', description="Function used for the selection of the quasi-identifying column target of the Mondrian cut", alias="columnScoringFunction")
    driver: SparkPodSpec
    executor: CommonJobExecutor
    is_fully_distributed: Optional[StrictBool] = Field(default=True, description="Enable distribution of the sanitization process from the early partitioning stages", alias="isFullyDistributed")
    input: StrictStr = Field(description="Input dataset")
    id_attributes: Optional[List[StrictStr]] = Field(default=None, description="Identifying attributes of the dataset", alias="idAttributes")
    information_loss_measures: Optional[List[StrictStr]] = Field(default=None, description="Functions to estimate the utility loss of the sanitized dataset", alias="informationLossMeasures")
    output: StrictStr = Field(description="Output dataset")
    partitions: Optional[Annotated[int, Field(strict=True, ge=1)]] = Field(default=None, description="Number of partitions distributed among the worker nodes")
    partition_function: Optional[StrictStr] = Field(default='mondrian', description="Function used for the initial partitioning of the dataset", alias="partitionFunction")
    quasi_id_attributes: Annotated[List[StrictStr], Field(min_length=1)] = Field(description="Quasi-identifying attributes of the dataset", alias="quasiIdAttributes")
    redact: Optional[StrictBool] = Field(default=False, description="Keep identifying attributes by redacting them")
    sampling_fraction: Optional[Union[Annotated[float, Field(le=1, strict=True, gt=0)], Annotated[int, Field(le=1, strict=True, gt=0)]]] = Field(default=1, description="Fraction of the dataset considered in the initial partitioning of the dataset", alias="samplingFraction")
    repartition_function: Optional[StrictStr] = Field(default='byRange', description="Function used for repartitioning the dataset among worker nodes", alias="repartitionFunction")
    k: Annotated[int, Field(strict=True, ge=1)] = Field(description="Privacy parameter determining the minimum size of equivalence classes in the sanitized dataset")
    __properties: ClassVar[List[str]] = ["columnScoringFunction", "driver", "executor", "isFullyDistributed", "input", "idAttributes", "informationLossMeasures", "output", "partitions", "partitionFunction", "quasiIdAttributes", "redact", "samplingFraction", "repartitionFunction", "k"]

    @field_validator('column_scoring_function')
    def column_scoring_function_validate_enum(cls, value):
        """Validates the enum"""
        if value is None:
            return value

        if value not in ('entropy', 'negativeEntropy', 'normalizedSpan', 'span'):
            raise ValueError("must be one of enum values ('entropy', 'negativeEntropy', 'normalizedSpan', 'span')")
        return value

    @field_validator('information_loss_measures')
    def information_loss_measures_validate_enum(cls, value):
        """Validates the enum"""
        if value is None:
            return value

        for i in value:
            if i not in ('discernabilityPenalty', 'globalCertaintyPenalty', 'normalizedCertaintyPenalty'):
                raise ValueError("each list item must be one of ('discernabilityPenalty', 'globalCertaintyPenalty', 'normalizedCertaintyPenalty')")
        return value

    @field_validator('partition_function')
    def partition_function_validate_enum(cls, value):
        """Validates the enum"""
        if value is None:
            return value

        if value not in ('mondrian', 'quantile'):
            raise ValueError("must be one of enum values ('mondrian', 'quantile')")
        return value

    @field_validator('repartition_function')
    def repartition_function_validate_enum(cls, value):
        """Validates the enum"""
        if value is None:
            return value

        if value not in ('byPartition', 'byRange', 'none'):
            raise ValueError("must be one of enum values ('byPartition', 'byRange', 'none')")
        return value

    model_config = {
        "populate_by_name": True,
        "validate_assignment": True,
        "protected_namespaces": (),
    }


    def to_str(self) -> str:
        """Returns the string representation of the model using alias"""
        return pprint.pformat(self.model_dump(by_alias=True))

    def to_json(self) -> str:
        """Returns the JSON representation of the model using alias"""
        # TODO: pydantic v2: use .model_dump_json(by_alias=True, exclude_unset=True) instead
        return json.dumps(self.to_dict())

    @classmethod
    def from_json(cls, json_str: str) -> Self:
        """Create an instance of KAnonymityJob from a JSON string"""
        return cls.from_dict(json.loads(json_str))

    def to_dict(self) -> Dict[str, Any]:
        """Return the dictionary representation of the model using alias.

        This has the following differences from calling pydantic's
        `self.model_dump(by_alias=True)`:

        * `None` is only added to the output dict for nullable fields that
          were set at model initialization. Other fields with value `None`
          are ignored.
        """
        _dict = self.model_dump(
            by_alias=True,
            exclude={
            },
            exclude_none=True,
        )
        # override the default output from pydantic by calling `to_dict()` of driver
        if self.driver:
            _dict['driver'] = self.driver.to_dict()
        # override the default output from pydantic by calling `to_dict()` of executor
        if self.executor:
            _dict['executor'] = self.executor.to_dict()
        return _dict

    @classmethod
    def from_dict(cls, obj: Dict) -> Self:
        """Create an instance of KAnonymityJob from a dict"""
        if obj is None:
            return None

        if not isinstance(obj, dict):
            return cls.model_validate(obj)

        _obj = cls.model_validate({
            "columnScoringFunction": obj.get("columnScoringFunction") if obj.get("columnScoringFunction") is not None else 'span',
            "driver": SparkPodSpec.from_dict(obj.get("driver")) if obj.get("driver") is not None else None,
            "executor": CommonJobExecutor.from_dict(obj.get("executor")) if obj.get("executor") is not None else None,
            "isFullyDistributed": obj.get("isFullyDistributed") if obj.get("isFullyDistributed") is not None else True,
            "input": obj.get("input"),
            "idAttributes": obj.get("idAttributes"),
            "informationLossMeasures": obj.get("informationLossMeasures"),
            "output": obj.get("output"),
            "partitions": obj.get("partitions"),
            "partitionFunction": obj.get("partitionFunction") if obj.get("partitionFunction") is not None else 'mondrian',
            "quasiIdAttributes": obj.get("quasiIdAttributes"),
            "redact": obj.get("redact") if obj.get("redact") is not None else False,
            "samplingFraction": obj.get("samplingFraction") if obj.get("samplingFraction") is not None else 1,
            "repartitionFunction": obj.get("repartitionFunction") if obj.get("repartitionFunction") is not None else 'byRange',
            "k": obj.get("k")
        })
        return _obj

