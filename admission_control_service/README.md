# Admission Control Service

This service validates the creation, modification and deletion of Kubernetes
resources within the Kubernetes cluster with the goal of meeting governance
and legal requirements, but also ensuring adherence to best practices and
institutional conventions.

## Overview

Kubernetes allows decoupling policy decisions from the inner workings of the
API server by means of admission controller webhooks, which are executed
whenever a resource is created, updated or deleted. This service provides
mutating and validating webhook that modify objects sent to the API server to
enforce custom defaults, or reject requests to enforce custom policies.

## Dependencies

The admission control service integrates by design with Kubernetes, the target
orchestration system of the GLACIATION platform. Indeed, by using
[Gatekeeper](https://github.com/open-policy-agent/gatekeeper), a customizable
cloud native policy controller that helps enforce policies executed by
[Open Policy Agent](https://github.com/open-policy-agent/opa), we can focus our
efforts in the configuration and definition of new policies.

## Architecture

![Image displaying the architecture of the service](docs/architecture.png)

Further details about the functioning of Gatekeeper can be found in the
[official documentation](https://open-policy-agent.github.io/gatekeeper/website/docs/operations).

## Terminology

| Term | Description |
|---|---|
| Admission controller | Component intercepting requests to the Kubernetes API server prior to persistence of the object |
| API server | Frontend to the cluster's shared state through which all Kubernetes components interact |
| Constraint | Enforce a ConstraintTemplate by specificying the kind of resources affected and the enforcement parameters |
| ConstraintTemplate | Definition of the Rego policy enforcing the policy and the schema of parameters to configure it |
| CustomResourceDefinition | Extension of the Kubernetes API not available in default Kubernetes installations |
| Mutating admission controller | Admission controllers that may modify objects related to the request they admit |
| Validating admission controller | Admission controllers that may not modify objects related to the request they admit |

## Gatekeeper's custom resources definitions

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
and the enforcement parameters. In this example, the constraint uses the
`K8sAllowedRepos` constraint template above to ensure pods deployed to the
default namespace come from the `openpolicyagent` image registry.

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
