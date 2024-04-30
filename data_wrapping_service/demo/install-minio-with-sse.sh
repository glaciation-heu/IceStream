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
echo -e '\n[-] Enable automated workflow authentication'
vault auth enable approle
echo -e '\n[-] Create the role of the KES server'
vault write auth/approle/role/kes-server token_num_uses=0  secret_id_num_uses=0  period=5m
echo -e '\n[-] Bind the KES server role to the KES policy'
vault write auth/approle/role/kes-server policies=kes-policy
echo -e '\n[-] Generate an identifier for the KES server'
# vault read auth/approle/role/kes-server/role-id
ROLE_ID=$(curl --cacert $VAULT_CACERT -H "X-Vault-Request: true" -H "X-Vault-Token: $VAULT_ROOT_TOKEN" $VAULT_ADDR/v1/auth/approle/role/kes-server/role-id | jq -r .data.role_id)
echo "role_id: $ROLE_ID"
echo -e '\n[-] Generate a secret for the KES server'
# vault write -f auth/approle/role/kes-server/secret-id
SECRET_ID=$(curl --cacert $VAULT_CACERT -X PUT -H "X-Vault-Request: true" -H "X-Vault-Token: $VAULT_ROOT_TOKEN" -d 'null' $VAULT_ADDR/v1/auth/approle/role/kes-server/secret-id | jq -r .data.secret_id)
echo "secret_id: $SECRET_ID"

# # Wait for interaction with the Vault HTTP API
# echo ''
# read -n 1 -srep '<<Press any key to continue>>'

sed "s/<VAULT SERVICE NAME>/$VAULT_SERVICE_NAME/g" minio-tenant-values-template.yaml > minio-tenant-values.yaml
sed -i "s/<VAULT K8S NAMESPACE>/$VAULT_K8S_NAMESPACE/g" minio-tenant-values.yaml
sed -i "s/<K8S CLUSTER NAME>/$K8S_CLUSTER_NAME/g" minio-tenant-values.yaml
sed -i "s/<APPROLE ROLE ID>/$ROLE_ID/g" minio-tenant-values.yaml
sed -i "s/<APPROLE SECRET ID>/$SECRET_ID/g" minio-tenant-values.yaml

echo -e '\n[*] Create MinIO tenant'
helm install \
  --namespace minio-tenant \
  --values minio-tenant-values.yaml \
  --create-namespace \
  tenant minio-operator/tenant

echo -e '\n[-] Patch Tenant to enforce the right volume permissions'
kubectl apply -f tenant-with-custom-initcontainers.yaml

echo -e '\nWaiting for the initialization of the MinIO tenant...'
kubectl wait -n minio-tenant --for=jsonpath='{.status.currentState}'=Initialized --timeout=120s tenant/myminio

echo -e '\n[-] Store Vault root certificate autority in the MinIO tenant'
kubectl create secret generic vault-tls -n minio-tenant --from-file=vault.ca=$VAULT_CACERT

echo -e '\n[-] Patch KES pods to trust the Vault certificate'
MINIO_KES_IDENTITY=$(kubectl get sts -n minio-tenant myminio-kes -o jsonpath={.spec.template.spec.containers[0].env[0].value})
sed "s/<MINIO KES IDENTITY>/$MINIO_KES_IDENTITY/g" kes-with-vault-certificate-template.yaml > kes-with-vault-certificate.yaml
kubectl apply -f kes-with-vault-certificate.yaml

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