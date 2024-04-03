# Data Wrapping Service

This service offers server-side encryption of object stores and Kubernetes
volumes, allowing clients to take advantage of server processing power to
secure resources at the storage layer (i.e., encryption at rest).

Encrypting object stores and Kubernetes volumes offers a robust shield for
sensitive data at rest. This not only safeguards information from unauthorized
individuals who gain physical access to storage disks or underlying nodes, but
also helps meet industry standards and regulations. By limiting the blast
radius of security incidents, it strengthens operational security and builds
trust with stakeholders.

## Demo

<p align="center">
  <a href="https://asciinema.org/a/f8reoNaOUtwuJSCJE5j2px5vl">
    <img alt=asciicast src="https://asciinema.org/a/f8reoNaOUtwuJSCJE5j2px5vl.svg" width="80%">
  </a>
</p>

## Installation

> NOTE: The installation procedure relies on the use of Helm charts, `kubectl`
> commands and `vault` commands. Therefore the installation of these CLI
> utilities is mandatory for the successful installation of the data wrapping
> service.

Run the following script to install the MinIO and Hashicorp Vault:

```shell
./install-minio-with-sse.sh
```

You can alter the variables in `demo/minio-tenant-values-template.yaml` and
`demo/vault-ha-values.yaml` to customize your deployment.

## Uninstallation

Run the following to uninstall MinIO and Hashicorp Vault:

```shell
helm uninstall --namespace minio-tenant tenant
helm uninstall --namespace minio-operator operator
helm uninstall --namespace vault vault
```

## How to use Server-Side Encryption (SSE)

### Object store interfaces :white_check_mark:

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

### Kubernetes persistent volume interface :construction_worker:

The following showcases basic usage of persistent volume claims by pods. For a
complete view of the details regarding persistent volumes please refer to the
official [documentation](https://kubernetes.io/docs/concepts/storage/persistent-volumes/).

#### PersistentVolumeClaim

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

#### Pod with a PersistentVolumeClaim

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
