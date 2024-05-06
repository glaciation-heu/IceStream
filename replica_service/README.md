# Replica Service

# MinIO deployment

## Dockerization service/component:

The docker images are provided by the minio.

## Helm Chart Deployment:

Add minio repo:
```bash
    helm repo add minio-repo https://operator.min.io
```

There are two helm charts for MinIO for operator and for tenant:

To install operator execute the following commands (Note the [operator.values.yaml](operator.values.yaml)):
```bash
    helm install minio-operator minio-repo/operator --create-namespace -n minio --values ./operator.values.yaml 
```

To install test tenant execute the following commands (Note the [tenant.values.yaml](tenant.values.yaml)):
```bash
    helm install test-tenant minio-repo/tenant --create-namespace -n test-tenant --values ./tenant.values.yaml 
```
## Accessing the tenant

```bash
    mc alias set test http://test-tenant.integration minio password
```

### List buckets
```bash
    mc ls test
```

### Copy to bucket
```bash
    mc cp <file> test/<bucket>
```
