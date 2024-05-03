#!/bin/bash

set -e

source install-cert-manager.sh

echo '[-] Install trust-manager'
helm repo add jetstack https://charts.jetstack.io --force-update
helm repo update jetstack
helm install \
  trust-manager jetstack/trust-manager \
  --namespace cert-manager \
  --set podDisruptionBudget.enabled=true \
  --set replicaCount=2 \
  --set secretTargets.enabled=true \
  --set secretTargets.authorizedSecrets[0]=ca-bundle \
  --version v0.9.2 \
  --wait

echo -e '\nWaiting for the rollout of trust-manager...'
kubectl -n cert-manager rollout status deploy/trust-manager

echo -e '\nSetup root certificate bundle'
kubectl create -f trust-manager-ca-bundle.yaml
echo ''
