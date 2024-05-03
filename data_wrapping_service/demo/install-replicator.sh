#!/bin/bash

set -e

echo '[-] Install replicator'
helm repo add mittwald https://helm.mittwald.de
helm repo update mittwald
helm install \
  kubernetes-replicator mittwald/kubernetes-replicator \
  --namespace replicator \
  --create-namespace \
  --version v2.9.2

echo -e '\nWaiting for the rollout of replicator...'
kubectl -n replicator rollout status deploy/kubernetes-replicator
