# Smoke tests

## Setup

The smoke tests have been automated with the definition of a Kubernetes Job
interacting with the MinIO tenant and data sanitization service APIs in order
to run a small data sanitization process (see [test](#test) for additional
details).

The Job has been configured to run after each Sync of the data sanitization
service with the use of the PostSync hook. On successful completion of the
hook, the Job is automatically removed from the cluster. So don't expect to see
it around unless something wrong has happened with the deployment of the
data sanitization service.

To see the declaration of the smoke tests head to the
[gitops-deployments](https://github.com/glaciation-heu/gitops-deployments/tree/main/integration/apps/security/data-sanitization-smoke-tests.yaml)
repository.

## Test

To verify the correct deployment of the data sanitization service we run a test
with [curl](https://curl.se/). But before that we need to setup the MinIO
tenant with the [MinIO client](https://min.io/docs/minio/linux/reference/minio-mc.html)
in order to use it for reading the input dataset and write the result of the
sanitization task.

So, first of all, we create an alias:

```bash
mc alias set minio https://minio.minio-tenant.svc.cluster.local $AWS_ACCESS_KEY_ID $AWS_SECRET_ACCESS_KEY
```

This specifies the endpoint of the MinIO tenant and the credentials to use for
the following interactions with it.

Then, we create the input and output buckets:

```bash
mc mb minio/sanitization/dataset
mc mb minio/sanitization/anonymized
```

And, we upload the input dataset to the `sanitization/dataset` bucket:

```bash
mc cp /tmp/adults.csv minio/sanitization/dataset/
```

Now, we send a request to the data sanitization service to start the
sanitization process:

```bash
curl \
    --silent \
    --request POST \
    --header 'Content-Type: application/json' \
    --data @/tmp/adults.json \
    http://data-sanitization.spark-app.svc.cluster.local/api/v1alpha1/job
```

And store the identifier of the request in `$REQ_ID`, then we check the status
of the data sanitization task:

```bash
curl \
    --silent \
    --request GET \
    --header 'Content-Type: application/json' \
    http://data-sanitization.spark-app.svc.cluster.local/api/v1alpha1/job/$REQ_ID/status
```

When the data sanitization process completes, we show part of the output:

```bash
PART=$(mc ls --json minio/sanitization/anonymized/adults.csv | jq -r '.key | select(startswith("part-00000-")) | select(endswith(".csv"))')
mc head minio/sanitization/anonymized/adults.csv/$PART
```

Finally, we delete the data sanitization task:

```bash
curl \
    --silent \
    --request DELETE \
    --header 'Content-Type: application/json' \
    --output /dev/null \
    http://data-sanitization.spark-app.svc.cluster.local/api/v1alpha1/job/$REQ_ID
```

When everything works smoothly we should see no errors with the execution of
the instructions, the data sanitization task reaches the `COMPLETED` status, and
we can see a snippet of the output dataset.
