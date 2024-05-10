# Smoke tests

## Setup

The smoke tests have been automated with the definition of a Kubernetes Job
interacting with the MinIO tenant API in order to create a few test resources
(see [tests](#tests) for additional details).

The Job has been configured to run after each Sync of the data wrapping
service with the use of the PostSync hook. On successful completion of the
hook, the Job is automatically removed from the cluster. So don't expect to see
it around unless something wrong has happened with the deployment of the
data wrapping service.

To see the declaration of the smoke tests head to the
[gitops-deployments](https://github.com/glaciation-heu/gitops-deployments/tree/main/integration/apps/minio-sse-smoke-tests.yaml)
repository.

## Tests

To verify the correct deployment of the data wrapping service we run a test
with [MinIO Client](https://min.io/docs/minio/linux/reference/minio-mc.html)
against the deployed MinIO tenant.

So, first of all, we create an alias:

```bash
mc alias set minio https://minio.minio-tenant.svc.cluster.local minio minio123
```

This specifies the endpoint of the MinIO tenant and the credentials to use for
the following interactions with it.

Then, we create a bucket:

```bash
mc mb minio/test-encrypted-bucket
```

And, we enable transparent encryption on it by using the default encryption key
created during the creation of the MinIO tenant (i.e., `encryption-key`):

```bash
mc encrypt set sse-kms encryption-key minio/test-encrypted-bucket
```

Now, we perform a series of operations to see the contents of the bucket,
create a new object, see the contents of the bucket and, finally, print the
contents of the object:

```bash
mc ls minio
echo "This is a line of text" > /tmp/test-object
mc mv /tmp/test-object minio/test-encrypted-bucket
mc ls minio/test-encrypted-bucket
mc cat minio/test-encrypted-bucket/test-object
```

When everything works smoothly we should see no errors with the execution of
these instructions.
