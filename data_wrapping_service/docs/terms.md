# Terminology

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
