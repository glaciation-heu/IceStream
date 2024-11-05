# Policies

## Resource requests and limits

### Overview

Kubernetes best practices dictate that resource limits and requests should
always be set on workloads (see [Kubernetes documentation](https://kubernetes.io/docs/concepts/configuration/manage-resources-containers/)).
Indeed, by specifying the resource *request* for containers in a Pod, the
kube-scheduler uses this information to decide which node to place the Pod on.
And, by specifying a resource *limit* for a container, the kubelet enforces
those limits so that the running container is not allowed to use more of that
resource than the set limit.
The kubelet also reserves at least the *request* amount of that system resource
specifically for that container to use.

> **Note:**
> If a limit is set, but no request is specified, and no admission-time
> mechanism has applied a default request for that resource, then Kubernetes
> copies the limit specified and uses it as the requested value for the
> resource.

#### CPU resource units

Limits and requests for CPU resources are measured in *cpu* units.
In Kubernetes, 1 CPU unit is equivalent to **1 physical CPU core**, or **1
virtual core**, depending on whether the node is a physical host or a virtual
machine running inside a physical machine.

Fractional requests are allowed, and their quantity is often expressed in
milliCPU.
For example, the quantity expression `0.1` is equivalent to the expression
`100m`.

#### Memory resource units

Limits and requests for *memory* are measured in bytes. The memory can be
expressed as a plain integer or as a fixed-point number using one of these
quantity suffixes: E, P, T, G, M, k. The power-of-two equivalents are also
available: Ei, Pi, Ti, Gi, Mi, Ki.

### Policy

Since setting resource requests and limits on all Pod can be a daunting task,
in the GLACIATION platform (see [set-default-resource-requests-and-limits.yaml](https://github.com/glaciation-heu/gitops-deployments/blob/main/base/apps/security/set-default-resource-requests-and-limits.yaml)
file), with the use of the Admission Control Service, we automate the
assignment of resource requests and limits by setting default values for cpu
and memory whenever they are missing.
The default values are the following:

| Resource | Request | Limits |
|----------|---------|--------|
| cpu      | 100m    | 1      |
| memory   | 256Mi   | 4Gi    |

Moreover, we also enforce the presence of the requests and limits (see
[validate-resource-requests-and-limits.yaml](https://github.com/glaciation-heu/gitops-deployments/blob/main/base/apps/security/validate-resource-requests-and-limits.yaml)
file), and their maximum allowed values by using validation rules from the
[OPA Gatekeeper Library](https://open-policy-agent.github.io/gatekeeper-library/website/).
The maximum values are the following:

| Resource | Request | Limits |
|----------|---------|--------|
| cpu      | 1       | 4Gi    |
| memory   | 2       | 8Gi    |

On request by the integration platform owners, this feature applies only to a
list of namespaces.
The current allowlist includes: `cert-manager`, `gatekeeper-system`,
`minio-operator`, `minio-tenant`, `replicator`, `spark-app`, `spark-operator`,
`vault`.

## Multi-tenant node isolation

### Overview

Sharing clusters saves costs and simplifies administration.
However, sharing clusters also presents challenges such as security, fairness,
and managing *noisy neighbors*.

*Multi-tenancy*, this is the term frequently used to describe sharing a cluster
among multiple end users or tenants, is a very recurring theme across multiple
use cases.
For example, in the GLACIATION platform, we can think of the project use cases
as different tenants of the platform.

While Kubernetes does not have first-class concepts of end users or tenants, it
provides several features to help manage different tenancy requirements.

#### Assigning Pods to Nodes

In Kubernetes, it is possible to constrain a Pod so that it is *restricted* to
run on particular node(s), or to *prefer* to run on particular nodes. There are
several ways to do this and the recommended approaches all use label selectors
to facilitate the selection.

`nodeSelector` is one of the recommended form of node selection constraint.
With the addition of the `nodeSelector` field to Pods, it is possible to
specify the desired node labels the target node should have.
Then, Kubernetes only schedules the Pod onto nodes that have a match with all
the requested labels.

### Policy

Considering the GLACIATION project use cases as different tenants of the
GLACIATION platform, we want to devise a policy that enforces node isolation
between their workloads.

As seen above, adding labels to nodes allows to target Pods for scheduling on
specific nodes or groups of nodes.
So, we can use this functionality to ensure that use cases' Pods only run on
nodes with certain isolation, security, or regulatory properties.
To facilitate adoption by use case partners, we use the Admission Control
Service to mutate Pods belonging to use-case-owned namespaces with the addition
of node selectors (see [set-multi-tenant-node-filtering.yaml](https://github.com/glaciation-heu/gitops-deployments/blob/main/base/apps/security/set-multi-tenant-node-filtering.yaml)).
Then, we ensure all Pods belonging to use-case-owned namespaces are indeed
using node selection by validating each Pod deployment (see
[validate-multi-tenant-node-filtering.yaml](https://github.com/glaciation-heu/gitops-deployments/blob/main/base/apps/security/validate-multi-tenant-node-filtering.yaml)).

This feature currently applies to `mef-sog-uc1-wl` and `uc2` namespaces.
