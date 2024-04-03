# Architecture

This service offers server-side encryption of object stores and Kubernetes
volumes, allowing clients to take advantage of server processing power to
secure resources at the storage layer (i.e., encryption at rest).

![Image displaying the architecture of the service](architecture.png)

Further details about the functioning of storage operators and, where
available, their integration with HashiCorp Vault can be found in the official
documentation of [Longhorn](https://longhorn.io/docs/1.7.0/advanced-resources/security/volume-encryption/),
[MinIO](https://min.io/docs/minio/kubernetes/upstream/administration/server-side-encryption.html),
and [Rook](https://rook.io/docs/rook/latest-release/Storage-Configuration/Advanced/key-management-system/#vault).

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
