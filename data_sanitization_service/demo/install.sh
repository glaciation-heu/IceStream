#!/bin/bash

set -e

echo '[*] Install MinIO object store'
PREV_PWD=$PWD
cd ../../data_wrapping_service/demo/
source install-minio-with-sse.sh ha
cd $PREV_PWD

echo -e '\n[*] Install Spark operator'
helm repo add spark-operator https://kubeflow.github.io/spark-operator/
kubectl create namespace spark-app
# TODO: Avoid allowing * verbs (see https://kubernetes.io/docs/concepts/security/rbac-good-practices/#escalate-verb)
helm install \
    --namespace spark-operator \
    --set webhook.enable=true \
    --set sparkJobNamespace=spark-app \
    --create-namespace \
    spark-operator spark-operator/spark-operator

echo -e '\nWaiting for the rollout of the Spark operator...'
kubectl -n spark-operator wait --for=condition=complete job/spark-operator-webhook-init
kubectl -n spark-operator rollout status deploy/spark-operator

echo -e '\n[*] Install Spark history server'
echo '[-] Configure object store for storing spark events'
mc alias set myminio https://$NODE_IP:$NODE_PORT minio minio123 --insecure
mc mb myminio/sanitization --insecure
mc mb myminio/sanitization/spark-events --insecure

echo -e '\n[-] Install Spark history server'
kubectl create secret generic minio-credentials \
    --namespace=spark-app \
    --from-literal=AWS_ACCESS_KEY_ID=minio \
    --from-literal=AWS_SECRET_ACCESS_KEY=minio123
kubectl create -f spark-history-server.yaml

echo -e '\nWaiting for the rollout of the Spark History Server...'
kubectl -n spark-app rollout status deploy/spark-history-server

echo -e '\n[-] Spark history server endpoint'
NODE_IP=$(kubectl get nodes --namespace spark-app -o jsonpath="{.items[0].status.addresses[0].address}")
NODE_PORT=$(kubectl get --namespace spark-app -o jsonpath="{.spec.ports[0].nodePort}" services spark-history-server)
echo "Serving Spark history server at http://$NODE_IP:$NODE_PORT"
