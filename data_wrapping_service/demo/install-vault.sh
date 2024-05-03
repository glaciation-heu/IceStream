#!/bin/bash

set -e

function unseal {
    for i in $(seq 0 $(($THRESHOLD-1)));
    do
        kubectl exec -n vault $1 -c vault -- vault operator unseal ${VAULT_UNSEAL_KEYS[$i]} > /dev/null
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

echo -e "\n[-] Install cert-manager"
source install-cert-manager.sh

echo '[-] Get certificate from our private certificate authority'
kubectl create -f vault-certificate.yaml

echo -e "\nWaiting for the creation of the certificate..."
kubectl wait -n vault --for=condition=Ready --timeout=120s certificate/vault-certificate

mkdir -p /tmp/vault
export WORKDIR=/tmp/vault
kubectl get secrets -n vault vault-tls -o 'jsonpath={.data.ca\.crt}' | base64 -d > $WORKDIR/ca.crt

echo -e "\n[-] Install $NAME with TLS"
helm repo add hashicorp https://helm.releases.hashicorp.com
helm install -n vault vault hashicorp/vault -f $VALUES

echo -e "\nWaiting for the rollout of $NAME..."
sleep 3 # wait for the StatefulSet to start the pods
kubectl -n vault wait --for=jsonpath='{.status.phase}'=Running --timeout=120s ${PODS[@]} # wait for the pods to reach running state

# Initialization
# TODO: Persist PGP encrypted Vault unseal keys somewhere outside the cluster
THRESHOLD=3
kubectl exec -n vault vault-0 -c vault -- vault operator init \
    -key-shares=5 \
    -key-threshold=$THRESHOLD \
    -format=json > $WORKDIR/cluster-keys.json
readarray -t VAULT_UNSEAL_KEYS <<<"$(jq -r '.unseal_keys_b64[]' $WORKDIR/cluster-keys.json)"
unseal vault-0

if [ $MODE = "ha" ]; then
    kubectl exec -n vault vault-1 -c vault -- /bin/sh -c 'vault operator raft join -address=https://vault-1.vault-internal:8200 -leader-ca-cert="$(cat /vault/userconfig/vault-tls/ca.crt)" -leader-client-cert="$(cat /vault/userconfig/vault-tls/tls.crt)" -leader-client-key="$(cat /vault/userconfig/vault-tls/tls.key)" https://vault-0.vault-internal:8200 > /dev/null'
    unseal vault-1
    kubectl exec -n vault vault-2 -c vault -- /bin/sh -c 'vault operator raft join -address=https://vault-2.vault-internal:8200 -leader-ca-cert="$(cat /vault/userconfig/vault-tls/ca.crt)" -leader-client-cert="$(cat /vault/userconfig/vault-tls/tls.crt)" -leader-client-key="$(cat /vault/userconfig/vault-tls/tls.key)" https://vault-0.vault-internal:8200 > /dev/null'
    unseal vault-2
fi
sleep 3 # wait for the unsealing

echo -e '\n[-] Vault endpoint'
NODE_IP=$(kubectl get nodes -o jsonpath="{.items[0].status.addresses[0].address}")
NODE_PORT=$(kubectl get -n vault -o jsonpath="{.spec.ports[0].nodePort}" services vault)
export VAULT_ROOT_TOKEN=$(jq -r '.root_token' $WORKDIR/cluster-keys.json)
echo "Serving Vault at https://$NODE_IP:$NODE_PORT"
echo "Token: $VAULT_ROOT_TOKEN"

# Setup environment variables of the vault CLI
export VAULT_ADDR="https://$NODE_IP:$NODE_PORT"
export VAULT_CACERT=$WORKDIR/ca.crt
