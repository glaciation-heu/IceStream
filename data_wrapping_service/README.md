# Data Wrapping Service

This service offers server-side encryption of object stores and Kubernetes
volumes, allowing clients to take advantage of server processing power to
secure resources at the storage layer (i.e., encryption at rest).

## Overview

Encrypting object stores and Kubernetes volumes offers a robust shield for
sensitive data at rest. This not only safeguards information from unauthorized
individuals who gain physical access to storage disks or underlying nodes, but
also helps meet industry standards and regulations. By limiting the blast
radius of security incidents, it strengthens operational security and builds
trust with stakeholders.

## Dependencies

To seamlessly integrate the wrapping service within Kubernetes, the target
orchestration system of the GLACIATION platform, we need the following
dependencies:

- First-party storage solution: A distributed storage solution supporting
  transparent encryption of object stores and persistent volumes within the
  Kubernetes cluster (e.g., [Longhorn](https://longhorn.io/),
  [MinIO](https://github.com/minio/operator),
  and [Rook](https://github.com/rook/rook))
- [HashiCorp Vault](https://github.com/hashicorp/vault): A tool for secrets
  management, encryption as a service, and privileged access management

## Architecture

![Image displaying the architecture of the service](docs/architecture.png)

Further details about the functioning of storage operators and, where
available, their integration with HashiCorp Vault can be found in the official
documentation of [Longhorn](https://longhorn.io/docs/1.7.0/advanced-resources/security/volume-encryption/),
[MinIO](https://min.io/docs/minio/kubernetes/upstream/administration/server-side-encryption.html),
and [Rook](https://rook.io/docs/rook/latest-release/Storage-Configuration/Advanced/key-management-system/#vault).

## Terminology

| Term | Description |
|---|---|
| Binding | One-to-one mapping between the PersistentVolumeClaim and its PersistentVolume |
| Block storage | Storage solution backed by a block device |
| Container Storage Interface (CSI) | Standard for exposing arbitrary block and file storage storage systems to containerized workloads |
| Container Object Storage Interface (COSI) | Set of abstractions for provisioning and management of object storage |
| File storage | Storage solution backed by a filesystem |
| Object storage | Storage solution promoting disaggregation of compute and storage by making data available over the network |
| PersistentVolume (PV) | Storage resource provisioned by an administrator or dynamically provisioned using Storage Classes |
| PersistentVolumeClaim (PVC) | Request for storage by a Pod |
| Provisioning | Process of assigning new storage resources to the cluster |
| Reclaim policy | What to do with the volume after it has been released of its claim (e.g., retain, delete) |
| ReadOnlyMany | Volume can be mounted as read-only by many nodes |
| ReadWriteMany | Volume can be mounted as read-write by many nodes |
| ReadWriteOnce | Volume can be mounted as read-write by a single node |
| ReadWriteOncePod | Volume can be mounted as read-write by a single Pod |
| Simple Storage Service (S3) API | Standard interface for the interaction with object storage services |
| Storage Class | Describe the class of storage (e.g., encrypted) |

## Object store interfaces

Despite the definition of the Container Object Storage Interface (COSI), not
all object storage providers support it. This means that depending on the
specific technology chosen for the implementation of the object store different
interfaces may be available.

Rook and MinIO provide WebUIs and S3-compatible REST APIs allowing for the
creation of object store resources. Moreover, by implementing the COSI
specification, Rook enables the creation of new object store buckets and the
management of their credentials within Kubernetes through Custom Resource
Definitions (CRDs). Additional information is available in the
[Rook documentation](https://rook.io/docs/rook/latest-release/Storage-Configuration/Object-Storage-RGW/object-storage/).

## Kubernetes persistent volume interface

The following showcases basic usage of persistent volume claims by pods. For a
complete view of the details regarding persistent volumes please refer to the
official [documentation](https://kubernetes.io/docs/concepts/storage/persistent-volumes/).

### PersistentVolumeClaim

```yaml
apiVersion: v1
kind: PersistentVolumeClaim
metadata:
  name: my-encrypted-volume-claim
spec:
  accessModes:
    - ReadWriteOnce
  resources:
    requests:
      storage: 4Gi
  storageClassName: encrypted
```

### Pod with a PersistentVolumeClaim

Pods access storage by using the claim as a volume. The cluster finds the claim
in the Pod's namespace and uses it to get the PersistentVolume backing the
claim. The volume is then mounted to the host and into the Pod.

```yaml
apiVersion: v1
kind: Pod
metadata:
  name: my-database
spec:
  containers:
    - name: postgres
      image: postgres
      volumeMounts:
      - mountPath: /var/lib/postgresql/data
        name: my-encrypted-volume
  volumes:
    - name: my-encrypted-volume
      persistentVolumeClaim:
        claimName: my-encrypted-volume-claim
```
