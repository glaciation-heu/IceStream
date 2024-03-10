# Admission Control Service

This service validates the creation, modification and deletion of Kubernetes
resources within the Kubernetes cluster with the goal of meeting governance
and legal requirements, but also ensuring adherence to best practices and
institutional conventions.

## Demo

<p align="center">
  <a href="https://asciinema.org/a/G1TUaJzR6q3kvk0cCZ8jBHxPx">
    <img alt=asciicast src="https://asciinema.org/a/G1TUaJzR6q3kvk0cCZ8jBHxPx.svg" width="80%">
  </a>
</p>

## Installation

A Helm chart exists in `code/service/charts/gatekeeper`. If you have Helm
installed, you can deploy via the following instructions for Helm v3:

```shell
helm repo add gatekeeper https://open-policy-agent.github.io/gatekeeper/charts
helm install gatekeeper/gatekeeper --name-template=gatekeeper --namespace gatekeeper-system --create-namespace
```

You can alter the variables in `code/service/charts/gatekeeper/values.yaml` to
customize your deployment. To regenerate the base template, run make manifests.

## Uninstallation

Run the following to uninstall Gatekeeper:

```shell
helm delete gatekeeper --namespace gatekeeper-system
```

Helm v3 will not cleanup Gatekeeper installed CRDs. Run the following to
uninstall Gatekeeper CRDs:

```shell
kubectl delete crd -l gatekeeper.sh/system=yes
```

This operation will also delete any user installed config changes, and
constraint templates and constraints.

## How to use Gatekeeper

The following section provides the basic details necessary to understand how to
interact with the Gatekeeper service. Additional details can be found in the
[Gatekeeper documentation](https://open-policy-agent.github.io/gatekeeper/website/docs/howto/).

### Constraint Templates

Before defining a constraint, it is necessary to declare its template, which
describes the Rego policy enforcing the constraint and the schema of its
parameters.

Here is an example constraint template that requires pods to be downloaded by a
list of allowed repositories:

```yaml
apiVersion: templates.gatekeeper.sh/v1
kind: ConstraintTemplate
metadata:
  name: k8sallowedrepos
  annotations:
    metadata.gatekeeper.sh/title: "Allowed Repositories"
    metadata.gatekeeper.sh/version: 1.0.1
    description: >-
      Requires container images to begin with a string from the specified list.
spec:
  crd:
    spec:
      names:
        kind: K8sAllowedRepos
      validation:
        # Schema for the `parameters` field
        openAPIV3Schema:
          type: object
          properties:
            repos:
              description: The list of prefixes a container image is allowed to have.
              type: array
              items:
                type: string
  targets:
    - target: admission.k8s.gatekeeper.sh
      rego: |
        package k8sallowedrepos

        violation[{"msg": msg}] {
          container := input.review.object.spec.containers[_]
          not strings.any_prefix_match(container.image, input.parameters.repos)
          msg := sprintf("container <%v> has an invalid image repo <%v>, allowed repos are %v", [container.name, container.image, input.parameters.repos])
        }
```

### Constraint

It enforces a ConstraintTemplate by specificying the kind of resources affected
and the enforcement parameters.

In this example, the constraint uses the `K8sAllowedRepos` constraint template
above to ensure pods deployed to the default namespace come from the
`openpolicyagent` image registry.

```yaml
apiVersion: constraints.gatekeeper.sh/v1beta1
kind: K8sAllowedRepos
metadata:
  name: repo-is-openpolicyagent
spec:
  match:
    kinds:
      - apiGroups: [""]
        kinds: ["Pod"]
    namespaces:
      - "default"
  parameters:
    repos:
      - "openpolicyagent/"
```

### Other example policies

Gatekeeper has a community-owned library of policies. So, you can find
other examples of validating and mutating policies in the `policy-library`.

## Web UI (optional)

Gatekeeper Policy Manager is a simple read-only web UI for viewing OPA
Gatekeeper policies' status in a Kubernetes Cluster.

GPM can display all the defined Constraint Templates with their rego code, all
the Gatekeeper Configuration CRDs, and all the Constraints with their current
status, violations, enforcement action, matches definitions, etc.

### Installation

A Helm chart exists in `code/web-ui/chart`.

First, to configure the installation, we suggest creating your own values file,
with your custom values for the release. See the [chart's readme](https://github.com/sighupio/gatekeeper-policy-manager/blob/5700a8174f3b31fb58dba595f3e997d4a323b44e/chart/README.md)
and the [default values.yaml](https://github.com/sighupio/gatekeeper-policy-manager/blob/5700a8174f3b31fb58dba595f3e997d4a323b44e/chart/values.yaml)
for more information.

> By default the value of the config.secretKey is set to null, this is
> an invalid value and should be overwritten with a secure string of your
> chosing.

Then, execute:

```shell
helm repo add gpm https://sighupio.github.io/gatekeeper-policy-manager
helm upgrade --install --namespace gatekeeper-system --set image.tag=v1.0.10 --values values.yaml gatekeeper-policy-manager gpm/gatekeeper-policy-manager
```

### Uninstallation

Run the following to uninstall Gatekeeper Policy Manager:

```shell
helm delete gatekeeper-policy-manager --namespace gatekeeper-system
```
