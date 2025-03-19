#!/bin/bash

set -e

. demo-magic.sh -n

# Speed at which to simulate typing
TYPE_SPEED=30

function print_section_title {
    echo -n $'\e[32;1m'
    echo -e "$1"
    echo -n $'\e[0m'
}

# By setting the KUBECONFIG environment variable it is possible to run the demo
# against different kubernetes environments

# Support selecting one of the available datasets
DATASET="${1:-adults}"
case $DATASET in
  adults) ;;
  poker) ;;
  *)
    echo 'Invalid demo dataset'
    exit 1
    ;;
esac

clear
wait # avoid seeing command prompt

print_section_title "[*] Let's see what is running in our Kubernetes cluster"
p 'kubectl get pods --all-namespaces --field-selector metadata.namespace!=kube-system'
kubectl get pods --all-namespaces --field-selector metadata.namespace!=kube-system,metadata.namespace!=vault

print_section_title '\n[*] External services'
pe 'NODE_IP=$(kubectl get nodes -o jsonpath="{.items[0].status.addresses[0].address}")'

print_section_title '\n[.] MinIO console'
pe 'NODE_PORT=$(kubectl get --namespace minio-tenant -o jsonpath="{.spec.ports[0].nodePort}" services myminio-console)'
pe 'echo "Serving MinIO console at https://$NODE_IP:$NODE_PORT"'

print_section_title '\n[.] Spark history server'
pe 'NODE_PORT=$(kubectl get --namespace spark-app -o jsonpath="{.spec.ports[0].nodePort}" services spark-history-server)'
pe 'echo "Serving Spark history server at http://$NODE_IP:$NODE_PORT"'

print_section_title '\n[.] Data sanitization'
pe 'NODE_PORT=$(kubectl get --namespace spark-app -o jsonpath="{.spec.ports[0].nodePort}" services data-sanitization)'
pe 'echo "Serving data sanitization service at http://$NODE_IP:$NODE_PORT"'

wait # show web interfaces

print_section_title '\n[*] Setup object store for the sanitization process'
p 'mc mb myminio/sanitization/dataset'
mc mb --insecure myminio/sanitization/dataset
p 'mc mb myminio/sanitization/anonymized'
mc mb --insecure myminio/sanitization/anonymized
p "mc cp ../code/spark-app/distributed/dataset/$DATASET.csv myminio/sanitization/dataset/"
mc cp --insecure ../code/spark-app/distributed/dataset/$DATASET.csv myminio/sanitization/dataset/

print_section_title '\n\n[*] Peak into the contents of the dataset'
p "mc head myminio/sanitization/dataset/$DATASET.csv"
mc head --insecure myminio/sanitization/dataset/$DATASET.csv

wait # see changes in the minio interface

print_section_title '\n[*] Run sanitization job'
pe "cat $DATASET.json"
p "curl --silent --request POST --header 'Content-Type: application/json' --data @$DATASET.json http://$NODE_IP:$NODE_PORT/api/v1alpha1/job"
OUTPUT=$(
    curl \
        --silent \
        --request POST \
        --header 'Content-Type: application/json' \
        --data @$DATASET.json \
        http://$NODE_IP:$NODE_PORT/api/v1alpha1/job
)
echo $OUTPUT
REQ_ID=$(echo $OUTPUT | jq -r .id)

print_section_title '\n[*] Wait for the completion of the job'
STATUS="UNKNOWN"
while [ "$STATUS" != "COMPLETED" ]; do
    # sleep 5
    p "curl --silent --request GET --header 'Content-Type: application/json' http://$NODE_IP:$NODE_PORT/api/v1alpha1/job/$REQ_ID/status"
    OUTPUT=$(
        curl \
            --silent \
            --request GET \
            --header 'Content-Type: application/json' \
            http://$NODE_IP:$NODE_PORT/api/v1alpha1/job/$REQ_ID/status
    )
    echo $OUTPUT
    STATUS=$(echo $OUTPUT | jq -r .state)
    # echo "Data sanitization job with id=$REQ_ID has status=$STATUS"
done

print_section_title '\n[*] Showcase a sample of the output'
p 'mc ls myminio/sanitization/anonymized'
mc ls --insecure myminio/sanitization/anonymized
p "mc ls myminio/sanitization/anonymized/$DATASET.csv"
mc ls --insecure myminio/sanitization/anonymized/$DATASET.csv
PART=$(mc ls --insecure --json myminio/sanitization/anonymized/$DATASET.csv |
       jq -r '.key | select(startswith("part-00000-")) | select(endswith(".csv"))')
p "mc head myminio/sanitization/anonymized/$DATASET.csv/$PART"
mc head --insecure myminio/sanitization/anonymized/$DATASET.csv/$PART

wait # see spark-app log & see the history server

print_section_title '\n[*] Delete sanitization job'
pe "curl --silent --request DELETE --header 'Content-Type: application/json' --output /dev/null http://$NODE_IP:$NODE_PORT/api/v1alpha1/job/$REQ_ID"

wait # avoid seeing command prompt
