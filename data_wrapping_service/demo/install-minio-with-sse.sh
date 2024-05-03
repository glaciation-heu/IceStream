#!/bin/bash

set -e

MODE="${1:-ha}"
case $MODE in
  ha)
    NAME='HA Vault cluster'
    ;;
  standalone)
    NAME='Vault standalone server'
    ;;
  *)
    echo 'Invalid Vault mode'
    exit 1
    ;;
esac

echo '[*] Install MinIO operator'
helm repo add minio-operator https://operator.min.io
helm install \
  --namespace minio-operator \
  --set console.enabled=false \
  --create-namespace \
  operator minio-operator/operator

echo -e '\nWaiting for the rollout of the MinIO operator...'
# kubectl -n minio-operator rollout status deploy/console
kubectl -n minio-operator rollout status deploy/minio-operator

# # Expose MinIO console with a NodePort service
# KUBE_EDITOR="sed -i s/ClusterIP/NodePort/g" kubectl -n minio-operator edit services console
# 
# echo -e '\n[*] MinIO console'
# export NODE_PORT=$(kubectl get --namespace minio-operator -o jsonpath="{.spec.ports[0].nodePort}" services console)
# export NODE_IP=$(kubectl get nodes --namespace minio-operator -o jsonpath="{.items[0].status.addresses[0].address}")
# echo "Serving MinIO console at http://$NODE_IP:$NODE_PORT"
# echo "JWT Access Token: $(kubectl -n minio-operator get secret console-sa-secret -o jsonpath="{.data.token}" | base64 --decode)"

echo -e "\n[*] Install HashiCorp $NAME with TLS"
source install-vault.sh $MODE

echo -e "\n[*] Configure Hashicorp $NAME for the integration with MinIO"
echo '[-] Login with the root token'
vault login $VAULT_ROOT_TOKEN
echo -e '\n[-] Enable K/V backend'
vault secrets enable -version=2 kv
echo -e '\n[-] Define the API paths the KES server can access'
vault policy write kes-policy kes-policy.hcl
echo -e '\n[-] Allow MinIO KES to delegate authorization request to Vault'
kubectl create -f minio-kes-sa-and-secrets.yaml
echo -e '\n[-] Enable automated workflow authentication'
vault auth enable kubernetes
echo -e '\n[-] Configure Vault communication with Kubernetes'
SA_JWT_TOKEN=$(kubectl -n minio-tenant get secret minio-kes-secret --output 'jsonpath={.data.token}' | base64 --decode)
SA_CA_CRT=$(kubectl config view --raw --minify --flatten --output 'jsonpath={.clusters[].cluster.certificate-authority-data}' | base64 --decode)
K8S_HOST=$(kubectl config view --raw --minify --flatten --output 'jsonpath={.clusters[].cluster.server}')
vault write auth/kubernetes/config \
    token_reviewer_jwt="$SA_JWT_TOKEN" \
    kubernetes_host="$K8S_HOST" \
    kubernetes_ca_cert="$SA_CA_CRT" \
    issuer="https://kubernetes.default.svc.cluster.local"
echo -e '\n[-] Create the KES server role and bind the KES policy to it'
vault write auth/kubernetes/role/minio-kes \
    bound_service_account_names=minio-kes \
    bound_service_account_namespaces=minio-tenant \
    policies=kes-policy \
    ttl=1h

echo -e '\n[*] Create MinIO tenant'
kubectl create -f tenant-with-custom-initcontainers.yaml

echo -e '\nWaiting for the initialization of the MinIO tenant...'
kubectl wait -n minio-tenant --for=jsonpath='{.status.currentState}'=Initialized --timeout=120s tenant/myminio

echo -e '\nWaiting for the rollout of the MinIO tenant...'
kubectl -n minio-tenant rollout status sts/myminio-kes
kubectl -n minio-tenant rollout status sts/myminio-pool-0

echo -e '\n[*] MinIO tenant console'
NODE_IP=$(kubectl get nodes --namespace minio-tenant -o jsonpath="{.items[0].status.addresses[0].address}")
NODE_PORT=$(kubectl get --namespace minio-tenant -o jsonpath="{.spec.ports[0].nodePort}" services myminio-console)
echo "Serving MinIO tenant console at https://$NODE_IP:$NODE_PORT"
echo 'Credentials: user=minio, password=minio123'

echo -e '\n[*] MinIO tenant S3 API'
NODE_IP=$(kubectl get nodes --namespace minio-tenant -o jsonpath="{.items[0].status.addresses[0].address}")
NODE_PORT=$(kubectl get --namespace minio-tenant -o jsonpath="{.spec.ports[0].nodePort}" services minio)
echo "Serving MinIO tenant S3 API at https://$NODE_IP:$NODE_PORT"
echo 'Credentials: user=minio, password=minio123'