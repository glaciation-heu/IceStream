# Smoke tests

## Setup

The smoke tests have been automated with the definition of a Kubernetes Job
interacting with the Kubernetes API server in order to create and delete all
the necessary resources (see [tests](#tests) for additional details).

The Job has been configured to run after each Sync of the admission control
service with the use of the PostSync hook. On successful completion of the
hook, the Job (and all the resources created for its functioning) are
automatically removed from the cluster. So don't expect to see them around
unless something wrong has happened with the deployment of the admission
control service.

To see the declaration of the smoke tests head to the
[gitops-deployments](https://github.com/glaciation-heu/gitops-deployments/tree/main/integration/apps/security/manual/gatekeeper-smoke-tests.yaml)
repository.

## Tests

> DISCLAIMER: This documentation has been realized stating from the
> community-owned library of policies for the OPA Gatekeeper project (in
> [policy-library](../policy-library)). Specifically, by using the
> [Allowed Repositories](https://open-policy-agent.github.io/gatekeeper-library/website/validation/allowedrepos)
> samples.

To verify the correct deployment of the admission control service we run a test
with the [constraint template](../README.md#constraint-templates) and
[constraint](../README.md#constraint) described in the docs.

So, first of all, we create the constraint template:

```bash
kubectl apply -f https://raw.githubusercontent.com/open-policy-agent/gatekeeper-library/master/library/general/allowedrepos/template.yaml
```

Then, we enforce it by creating the constraint:

```bash
kubectl apply -f https://raw.githubusercontent.com/open-policy-agent/gatekeeper-library/master/library/general/allowedrepos/samples/repo-must-be-openpolicyagent/constraint.yaml
```

Now, we make sure the constraint is enforced by running a set of sample
deployments.

### Pod with Open Policy Agent container

Pod configuration:

```yaml
apiVersion: v1
kind: Pod
metadata:
  name: opa-allowed
spec:
  containers:
    - name: opa
      image: openpolicyagent/opa:0.9.2
      args:
        - "run"
        - "--server"
        - "--addr=localhost:8080"
      resources:
        limits:
          cpu: "100m"
          memory: "30Mi"
```

Deployed with:

```bash
kubectl apply -f https://raw.githubusercontent.com/open-policy-agent/gatekeeper-library/master/library/general/allowedrepos/samples/repo-must-be-openpolicyagent/example_allowed.yaml
```

Expectation: The Pod should succeed since the only container being deployed
comes from the trusted `openpolicyagent` registry.

### Pod with NGINX container

Pod configuration:

```yaml
apiVersion: v1
kind: Pod
metadata:
  name: nginx-disallowed
spec:
  containers:
    - name: nginx
      image: nginx
      resources:
        limits:
          cpu: "100m"
          memory: "30Mi"
```

Deployed with:

```bash
kubectl apply -f https://raw.githubusercontent.com/open-policy-agent/gatekeeper-library/master/library/general/allowedrepos/samples/repo-must-be-openpolicyagent/example_disallowed_container.yaml
```

Expectation: The request of creating the Pod should fail since the NGINX image
does not come from a registry belonging to the list of allowed registries.

### Pod with NGINX init container and Open Policy Agent container

Pod configuration:

```yaml
apiVersion: v1
kind: Pod
metadata:
  name: nginx-disallowed
spec:
  initContainers:
    - name: nginxinit
      image: nginx
      resources:
        limits:
          cpu: "100m"
          memory: "30Mi"
  containers:
    - name: opa
      image: openpolicyagent/opa:0.9.2
      args:
        - "run"
        - "--server"
        - "--addr=localhost:8080"
      resources:
        limits:
          cpu: "100m"
          memory: "30Mi"
```

Deployed with:

```bash
kubectl apply -f https://raw.githubusercontent.com/open-policy-agent/gatekeeper-library/master/library/general/allowedrepos/samples/repo-must-be-openpolicyagent/example_disallowed_initcontainer.yaml
```

Expectation: The request of creating the Pod should fail since the NGINX image
(of the init container) does not come from a registry belonging to the list of
allowed registries.

### Pod with NGINX init container and NGINX container

Pod configuration:

```yaml
apiVersion: v1
kind: Pod
metadata:
  name: nginx-disallowed
spec:
  initContainers:
  - name: nginxinit
    image: nginx
    resources:
      limits:
        cpu: "100m"
        memory: "30Mi"
  containers:
    - name: nginx
      image: nginx
      resources:
        limits:
          cpu: "100m"
          memory: "30Mi"
```

Deployed with:

```bash
kubectl apply -f https://raw.githubusercontent.com/open-policy-agent/gatekeeper-library/master/library/general/allowedrepos/samples/repo-must-be-openpolicyagent/example_disallowed_both.yaml
```

Expectation: The request of creating the Pod should fail since both the init
container and the container itself use the NGINX image belonging to the Docker
Hub registry (not listed in the allowed registries).

### Clean up

Delete every resource created (or tried to be created) during the test:

```bash
kubectl delete -f https://raw.githubusercontent.com/open-policy-agent/gatekeeper-library/master/library/general/allowedrepos/samples/repo-must-be-openpolicyagent/example_allowed.yaml
kubectl delete --ignore-not-found=true -f https://raw.githubusercontent.com/open-policy-agent/gatekeeper-library/master/library/general/allowedrepos/samples/repo-must-be-openpolicyagent/example_disallowed_container.yaml
kubectl delete --ignore-not-found=true -f https://raw.githubusercontent.com/open-policy-agent/gatekeeper-library/master/library/general/allowedrepos/samples/repo-must-be-openpolicyagent/example_disallowed_initcontainer.yaml
kubectl delete --ignore-not-found=true -f https://raw.githubusercontent.com/open-policy-agent/gatekeeper-library/master/library/general/allowedrepos/samples/repo-must-be-openpolicyagent/example_disallowed_both.yaml
kubectl delete -f https://raw.githubusercontent.com/open-policy-agent/gatekeeper-library/master/library/general/allowedrepos/samples/repo-must-be-openpolicyagent/constraint.yaml;
kubectl delete -f https://raw.githubusercontent.com/open-policy-agent/gatekeeper-library/master/library/general/allowedrepos/template.yaml
```
