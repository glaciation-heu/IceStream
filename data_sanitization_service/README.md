# Data Sanitization Service

This service implements an efficient and effective approach to protect users
data by obfuscating information that can disclose their identities and
sensitive information.

## Overview

To scale the computation of the sanitized dataset to datasets of significant
sizes, our service operates on the input dataset in a distributed manner.

Three kind of transformations are supported: k-anonymity, l-diversity, and the
use of both of them. Sanitization jobs are configured by the requesting
application with numerous parameters with the goal of tailoring the
sanitization process according to the specific requirements of the application.
These parameters include the input and the output; the classification of
attributes in identifiers, quasi-identifiers and sensitive attrubutes;
k-anonimity and l-diversity privacy parameters; the function used for
determining the dataset cuts; the set of custom generalization methods for
quasi-identifiers (if any); and the list of information loss metrics to
compute.

We also provide parameters to configure the process of distributing the dataset
among the worker nodes. Specifically, we provide a way to declare the fraction
of the dataset to be considered in this initial stage, the number of
partitions, the fragmentation strategy, and its parallelization and
repartitioning scheme.

Here a complete list of the parameters available:

| Parameter | Type | Description |
|---|---|---|
| input | URL | Input dataset |
| output | URL | Output dataset |
| id_columns | List of strings | Identifying attributes of the dataset |
| redact | Boolean | Flag to enable redaction of the identifying columns (if not enabled the identifying columns are removed) |
| quasiid_columns | List of strings | Quasi-identifying attributes of the dataset |
| quasiid_generalizations | List of objects | Advanced generalization of a specific quasi-identifying attribute |
| sensitive_columns | List of strings | Sensitive attributes of the dataset |
| column_score | String | Function to use for the selection of the quasi-identifying column target of the Mondrian cut (i.e., span, entropy, neg_entropy, norm_span) |
| K | Integer | Privacy parameter determining the minimum size of equivalence classes in the k-anonymity transformation |
| L | Integer | Privacy parameter determining the minimum number of distinct sensible values belonging to the equivalence class in the l-diversity transformation |
| fraction | Float | Fraction of the dataset to be considered in the early stages of the sanitization process during the distribution of the dataset to the Spark workers |
| fragments | Int | Number of fragments to be distributed among the Spark workers |
| fragmentation | String | Function to use for the identification of the fragments (i.e., mondrian, quantile) |
| parallel | Boolean | Flag to enable complete parallelization of the sanitization process (including the early stages to identify the fragments) |
| repartition | String | Function to use for repartitioning the dataset among the Spark workers |
| measures | List of strings | Functions to roughly measure the quality of the anonymized dataset (i.e., discernability_penalty, global_certainty_penalty, normalized_certainty_penalty) |

## Dependencies

The sanitization service is an Apache Spark application. To seemlessly
integrate it within Kubernetes, the target orchestration system of the
GLACIATION platform, we need the following dependencies:

- First/Third party object store: An object store for persisting the input and
  the output datasets either within the Kubernetes cluster deployed with a
  native Kubernetes operator (e.g., [MinIO](https://github.com/minio/operator),
  [Rook](https://github.com/rook/rook)) or outside the cluster by referencing
  an external object store
- [spark-on-k8s-operator](https://github.com/GoogleCloudPlatform/spark-on-k8s-operator):
  Kubernetes operator for managing the lifecycle of Apache Spark applications
  on Kubernetes
