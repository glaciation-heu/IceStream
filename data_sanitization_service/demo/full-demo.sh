#!/bin/bash

set -e

DATASET="${1:-adults}"
case $DATASET in
  adults) ;;
  poker) ;;
  *)
    echo 'Invalid demo dataset'
    exit 1
    ;;
esac

echo -e '[*] Install data sanitization service'
source install.sh

# Run data sanitization job
echo -e '\n[*] Demo'
source demo.sh $DATASET

# Wait cluster cleanup
echo ''
read -n 1 -srep '<<Press any key to continue>>'

echo -e '\n[*] Uninstall the data sanitization service'
kubectl delete -f ../code/rest-api/k8s-deployment.yaml

echo -e '\n[*] Uninstall Spark history server'
kubectl delete -f spark-history-server.yaml

echo -e '\n[*] Uninstall Spark operator'
helm uninstall --namespace spark-operator spark-operator

echo -e '\n[*] Uninstall MinIO tenant'
helm uninstall --namespace minio-tenant tenant

echo -e "\n[*] Uninstall HashiCorp Vault"
helm uninstall --namespace $VAULT_K8S_NAMESPACE $VAULT_HELM_RELEASE_NAME

echo -e '\n[*] Uninstall MinIO operator'
helm uninstall --namespace minio-operator operator
