#!/bin/bash

set -e

echo '[-] Install cert-manager'
helm repo add jetstack https://charts.jetstack.io --force-update
helm repo update jetstack
helm install \
  cert-manager jetstack/cert-manager \
  --namespace cert-manager \
  --create-namespace \
  --version v1.14.5 \
  --set installCRDs=true

echo -e '\nWaiting for the rollout of cert-manager...'
kubectl -n cert-manager rollout status deploy/cert-manager deploy/cert-manager-cainjector deploy/cert-manager-webhook

echo -e '\nSetup self-signed certificate authority of the cluster'
kubectl create -f selfsigned-ca.yaml
