# Data Sanitization Service

This service implements an efficient and effective approach to protect user
privacy by obfuscating their identities or sensitive information.

## Overview

To scale the computation of the sanitized dataset to datasets of significant
sizes, our service operates on the input dataset in a distributed manner.

Three kind of transformations are supported: k-anonymity, l-diversity, and the
use of both of them. Sanitization jobs are configured by the requesting
application with numerous parameters with the goal of tailoring the
sanitization process according to the specific requirements of the application.
These parameters include the input and the output; the classification of
attributes in identifiers, quasi-identifiers and sensitive attributes;
k-anonymity and l-diversity privacy parameters; the function used for
determining the dataset cuts; the set of custom generalization methods for
quasi-identifiers (if any); and the list of information loss metrics to
compute.

The anonymization and obfuscation process leverages the availability of a
distributed architecture of workers. The service enables the configuration of
data distribution and processing, through several parameters. In particular,
parameters include the specification of the fraction of the original dataset to
be considered in this initial stage, the number of partitions, the
fragmentation strategy, and its parallelization and repartitioning scheme.

### Assumptions

The input dataset target of the sanitization process MUST be in tabular
format. However, thanks to the use of Apache Spark, the sanitization service
can support multiple data formats (e.g., Avro, CSV, Delta, Iceberg, Parquet,
and ORC). The selection of the specific parsing and serialization format
depends on the extension of the dataset.

The support of quasi-identifier and sensitive attributes with complex object
types is not supported out of the box. For these use cases consider flattening
the object in multiple distinct attributes when feasible, and introduce ad hoc
changes to the sanitization service otherwise.

## Installation

> NOTE: The installation procedure relies on the use of Helm charts, `kubectl`,
> `vault` and `mc` commands. Therefore the installation of these CLI utilities
> is mandatory for the successful installation of the data sanitization
> service.

Run the following script to install the data sanitization service and all its
requirements:

```shell
./install.sh
```

## Uninstallation

Run the following to uninstall the data sanitization service and all its
requirements:

```shell
kubectl delete -f ../code/rest-api/k8s-deployment.yaml
kubectl delete -f spark-history-server.yaml
helm uninstall --namespace spark-operator spark-operator
helm uninstall --namespace minio-tenant tenant
helm uninstall --namespace vault vault
helm uninstall --namespace minio-operator operator
```

## How to use the data sanitization service

A concise overview of the service interface follows. For a complete view
including all the details see the [OpenAPI specification](docs/openapi.yaml).

### Data sanitization job creation

Create a job by submitting the desired data sanitization configuration.

Here is an example of a minimal configuration:

```json
{
    "driver": { "memory": "1g" },
    "executor": { "instances": 4, "memory": "1g" },
    "input": "s3a://sanitization/dataset/adults.csv",
    "k": 3,
    "output": "s3a://sanitization/anonymized/adults.csv",
    "quasiIdAttributes": [ "age", "education-num", "race", "native-country" ]
}
```

Assuming we are storing the configuration of the job in the `adults.json` file,
here is how we could interact with the data sanitization service:

```shell
    curl \
        --silent \
        --request POST \
        --header 'Content-Type: application/json' \
        --data @adults.json \
        http://$IP:$PORT/api/v1alpha1/job
```

This returns a JSON object including information about the identifier of the
created job. On successful invocation of the service interface the service
returns something like this:

```json
{"id": "27bb4c01-efb5-4617-8df5-17ea426e601b"}
```

### Data sanitization job status information

Use the identifier returned by the job creation to gather information about the
status of the job.

```shell
curl \
    --silent \
    --request GET \
    --header 'Content-Type: application/json' \
    http://$IP:$PORT/api/v1alpha1/job/$JOB_ID/status
```

This returns a JSON object including information about the state and a possible
error message. On successful completion of the job the service returns:

```json
{
  "errorMessage": "",
  "state": "COMPLETED"
}
```

### Data sanitization job deletion

Use the identifier returned by the job creation to delete the job and free
resources associated with its execution.

```shell
curl \
    --silent \
    --request DELETE \
    --header 'Content-Type: application/json' \
    --output /dev/null \
    http://$IP:$PORT/api/v1alpha1/job/$JOB_ID
```

This returns does not return any data.

## Publications

Additional information about the functioning of the service and its performance
against different datasets can be found in the following publications:

- [1] Sabrina De Capitani di Vimercati, Dario Facchinetti, Sara Foresti,
  Gianluca Oldani, Stefano Paraboschi, Matthew Rossi, Pierangela Samarati,
  **Scalable Distributed Anonymization Processing of Sensors Data**,
  in *Proceedings of the 19th IEEE International Conference on Pervasive
  Computing and Communications (PerCom)*, March 22-26, 2021
- [2] Sabrina De Capitani di Vimercati, Dario Facchinetti, Sara Foresti,
  Gianluca Oldani, Stefano Paraboschi, Matthew Rossi, Pierangela Samarati,
  **Artifact: Scalable Distributed Anonymization Processing of Sensors Data**,
  in *Proceedings of the 19th IEEE International Conference on Pervasive
  Computing and Communications (PerCom)*, March 22-26, 2021
- [3] Sabrina De Capitani di Vimercati, Dario Facchinetti, Sara Foresti,
  Giovanni Livraga, Gianluca Oldani, Stefano Paraboschi, Matthew Rossi,
  Pierangela Samarati, **Scalable Distributed Data Anonymization for Large
  Datasets**, in *IEEE Transactions on Big Data (TBD)*, June 01, 2023
