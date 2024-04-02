#!/bin/bash

set -e

function unseal {
    for i in $(seq 0 $(($THRESHOLD-1)));
    do
        kubectl exec -n $VAULT_K8S_NAMESPACE $1 -- vault operator unseal ${VAULT_UNSEAL_KEYS[$i]} > /dev/null
    done
}

MODE="${1:-ha}"
case $MODE in
    ha)
        NAME='HA Vault cluster'
        VALUES='vault-ha-values.yaml'
        PODS=('po/vault-0' 'po/vault-1' 'po/vault-2')
        ;;
    standalone)
        NAME='Vault standalone server'
        VALUES='vault-standalone-values.yaml'
        PODS=('po/vault-0')
        ;;
    *)
        echo 'Invalid Vault mode'
        exit 1
        ;;
esac

mkdir -p /tmp/vault

export VAULT_K8S_NAMESPACE="vault"
export VAULT_HELM_RELEASE_NAME="vault"
export VAULT_SERVICE_NAME="vault-internal"
export K8S_CLUSTER_NAME="cluster.local"
export WORKDIR=/tmp/vault

echo '[-] Create key and certificate signed by the K8s certificate authority'
openssl genrsa -out ${WORKDIR}/vault.key 2048
cat > ${WORKDIR}/vault-csr.conf <<EOF
[req]
default_bits = 2048
prompt = no
encrypt_key = yes
default_md = sha256
distinguished_name = kubelet_serving
req_extensions = v3_req
[ kubelet_serving ]
O = system:nodes
CN = system:node:*.${VAULT_K8S_NAMESPACE}.svc.${K8S_CLUSTER_NAME}
[ v3_req ]
basicConstraints = CA:FALSE
keyUsage = nonRepudiation, digitalSignature, keyEncipherment, dataEncipherment
extendedKeyUsage = serverAuth, clientAuth
subjectAltName = @alt_names
[alt_names]
DNS.1 = *.${VAULT_SERVICE_NAME}
DNS.2 = *.${VAULT_SERVICE_NAME}.${VAULT_K8S_NAMESPACE}.svc.${K8S_CLUSTER_NAME}
DNS.3 = *.${VAULT_K8S_NAMESPACE}
DNS.4 = ${VAULT_SERVICE_NAME}.${VAULT_K8S_NAMESPACE}.svc.${K8S_CLUSTER_NAME}
IP.1 = 127.0.0.1
IP.2 = $(kubectl get nodes -o jsonpath='{.items[0].status.addresses[0].address}')
EOF
openssl req -new -key ${WORKDIR}/vault.key -out ${WORKDIR}/vault.csr -config ${WORKDIR}/vault-csr.conf
cat > ${WORKDIR}/csr.yaml <<EOF
apiVersion: certificates.k8s.io/v1
kind: CertificateSigningRequest
metadata:
    name: vault.svc
spec:
    signerName: kubernetes.io/kubelet-serving
    expirationSeconds: 8640000
    request: $(base64 ${WORKDIR}/vault.csr | tr -d '\n')
    usages:
    - digital signature
    - key encipherment
    - server auth
EOF
kubectl create -f ${WORKDIR}/csr.yaml
kubectl certificate approve vault.svc

echo -e '\n[-] Store key, certificate, and certificate authority in the K8s secrets store'
kubectl get csr vault.svc -o jsonpath='{.status.certificate}' | base64 -d > ${WORKDIR}/vault.crt
kubectl config view --raw --minify --flatten -o jsonpath='{.clusters[].cluster.certificate-authority-data}' | base64 -d > ${WORKDIR}/vault.ca
kubectl create namespace ${VAULT_K8S_NAMESPACE}
kubectl create secret generic vault-tls \
    -n ${VAULT_K8S_NAMESPACE} \
    --from-file=vault.key=${WORKDIR}/vault.key \
    --from-file=vault.crt=${WORKDIR}/vault.crt \
    --from-file=vault.ca=${WORKDIR}/vault.ca

echo -e "\n[-] Install $NAME with TLS"
helm repo add hashicorp https://helm.releases.hashicorp.com
helm install -n $VAULT_K8S_NAMESPACE $VAULT_HELM_RELEASE_NAME hashicorp/vault -f $VALUES

echo -e "\nWaiting for the rollout of $NAME..."
sleep 3 # wait for the StatefulSet to start the pods
kubectl -n vault wait --for=jsonpath='{.status.phase}'=Running --timeout=60s ${PODS[@]} # wait for the pods to reach running state

# Initialization
THRESHOLD=3
kubectl exec -n $VAULT_K8S_NAMESPACE vault-0 -- vault operator init \
    -key-shares=5 \
    -key-threshold=$THRESHOLD \
    -format=json > ${WORKDIR}/cluster-keys.json
readarray -t VAULT_UNSEAL_KEYS <<<"$(jq -r '.unseal_keys_b64[]' /tmp/vault/cluster-keys.json)"
unseal vault-0

if [ $MODE = "ha" ]; then
    kubectl exec -n $VAULT_K8S_NAMESPACE vault-1 -- /bin/sh -c 'vault operator raft join -address=https://vault-1.vault-internal:8200 -leader-ca-cert="$(cat /vault/userconfig/vault-tls/vault.ca)" -leader-client-cert="$(cat /vault/userconfig/vault-tls/vault.crt)" -leader-client-key="$(cat /vault/userconfig/vault-tls/vault.key)" https://vault-0.vault-internal:8200 > /dev/null'
    unseal vault-1
    kubectl exec -n $VAULT_K8S_NAMESPACE vault-2 -- /bin/sh -c 'vault operator raft join -address=https://vault-2.vault-internal:8200 -leader-ca-cert="$(cat /vault/userconfig/vault-tls/vault.ca)" -leader-client-cert="$(cat /vault/userconfig/vault-tls/vault.crt)" -leader-client-key="$(cat /vault/userconfig/vault-tls/vault.key)" https://vault-0.vault-internal:8200 > /dev/null'
    unseal vault-2
fi
sleep 3 # wait for the unsealing

echo -e '\n[-] Vault endpoint'
export NODE_IP=$(kubectl get nodes -o jsonpath="{.items[0].status.addresses[0].address}")
export NODE_PORT=$(kubectl get -n $VAULT_K8S_NAMESPACE -o jsonpath="{.spec.ports[0].nodePort}" services vault)
export VAULT_ROOT_TOKEN=$(jq -r '.root_token' $WORKDIR/cluster-keys.json)
echo "Serving Vault at https://$NODE_IP:$NODE_PORT"
echo "Token: $VAULT_ROOT_TOKEN"

# Setup environment variables of the vault CLI
export VAULT_ADDR="https://$NODE_IP:$NODE_PORT"
export VAULT_CACERT=$WORKDIR/vault.ca
