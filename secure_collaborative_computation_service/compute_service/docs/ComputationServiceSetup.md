# Setup of the Computation Service
The Computation Service is realized with [Carbyne Stack](https://carbynestack.io).
(Currently, Carbyne Stack has to be setup manually, the plan is to fully automate this process in the future.)

## Local Setup
For a local setup with kind (Kubernetes in Docker), follow the [Carbyne Stack Getting Started Guide](https://carbynestack.io/getting-started).
There are currently two options:
- [Infrastructure As Code](https://carbynestack.io/getting-started/deployment/infrastructure-as-code/#stacks), which automates every step of the setup process. (Non-local deployment, i.e, without kind, is still a work-in-progress.)
- Manual setup as in the [installation guide](https://carbynestack.io/getting-started/deployment/manual/).

## Cloud Setup
For a cloud setup, we create Kubernetes environments via Gardener.
[Gardener](https://github.com/gardener/gardener) is a tool to simplify the creation and maintenance of Kubernetes environments on different cloud providers (e.g., AWS and Azure).
In Gardener, so-called shoots are created which describe the Kubernetes cluster (e.g., which cloud provider should be used, how many compute instance are needed). Thees shoots are configurable with the help of the Gardener dashboard (a web interface) or through the Kubernetes API.

Next, we describe how to create clusters for AWS (via Gardener) and then setup Carbyne Stack on the created cluster.

### Create clusters via Gardener Dashboard
1. Click on the `+` symbol on the top-right of the `CLUSTER` overview.
2. Select `AWS` as `Infrastructure`
3. Cluster details
    * Choose a name and select testing as Purpose.
    * Kubernetes version: 1.26.3, later versions should work as well.
4. Infrastructure Details
    * select the Secret for the AWS instance.
    * Select a region, tested on eu-west-1
    * Network Type: `calico`
5. Worker
    * Machine Type: `c5.2xlarge` (8 CPUs + 16GiB Memory)
6. Hibernation
    * On hibernation the cluster IP addresses change. Because of this it is better to remove the default hibernation schedule. (However, removing hibernation incurs additional costs.)
7. Click on `CREATE` and wait until the cluster was created.
For detail setup steps via Gardener (including setting up AWS secrets), visit the [official gardener documentation](https://github.com/gardener/gardener-extension-provider-aws/blob/master/docs/tutorials/kubernetes-cluster-on-aws-with-gardener/kubernetes-cluster-on-aws-with-gardener.md).

### Setup Carbyne Stack (on cluster created via Gardener)
To manually create the instance, follow the [manual installation guide](https://carbynestack.io/getting-started/deployment/manual/) with a few additions:
1. Since all cloud providers have their own LoadBalancer implementations, the section in the documentation where [MetallLB is installed](https://carbynestack.io/getting-started/deployment/manual/platform-setup/#metallb) can be ignored.
2. AWS assignes hostnames instead of public IPs to LoadBalancers. It is currently not possible to use thees hostnames for CarbyneStack, therefore before [installing knative](https://carbynestack.io/getting-started/deployment/manual/platform-setup/#knative) use
```bash
host $(kubectl get services --namespace istio-system istio-ingressgateway --output jsonpath='{.status.loadBalancer.ingress[0].hostname}') | head -n 1 | awk "{print \$NF}"
```
to get the public IP. Make sure this IP is already assigned by checking the `istio-ingressgateway` service (`kubectl get service --namespace istio-systen istio-ingressgateway`).

This setup should also work on kubernetes environments created with `AWS Eks`.