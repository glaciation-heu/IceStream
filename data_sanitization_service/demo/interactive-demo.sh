#!/bin/bash

set -e

. demo-magic.sh -n

# Speed at which to simulate typing
TYPE_SPEED=30

function cleanup {
    print_section_title '\n[*] Delete sanitization job'
    p "curl --silent --request DELETE --header 'Content-Type: application/json' --output /dev/null $URL/api/v1alpha1/job/$REQ_ID"
    curl --insecure --silent --request DELETE --header 'Content-Type: application/json' --output /dev/null $URL/api/v1alpha1/job/$REQ_ID
}

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

print_section_title "[*] Let's see what is running in the Kubernetes cluster"
print_section_title "\n[.] Namespace: data-wrapping"
pe 'kubectl get pods --namespace data-wrapping'
print_section_title "\n[.] Namespace: spark-app"
pe 'kubectl get pods --namespace spark-app'

print_section_title '\n[*] External services'

print_section_title '\n[.] MinIO'
if [[ $LOCAL ]]; then
    pe 'NODE_IP=$(kubectl get nodes -o jsonpath="{.items[0].status.addresses[0].address}")'
    pe 'NODE_PORT=$(kubectl get --namespace minio-tenant -o jsonpath="{.spec.ports[0].nodePort}" services minio)'
    pe 'MINIO_URL="https://$NODE_IP:$NODE_PORT"'
else
    pe 'export MINIO_URL=https://$(kubectl get ingress -n data-wrapping glaciation -o jsonpath="{.spec.rules[0].host}")'
fi
pe 'echo "Serving MinIO at $MINIO_URL"'

print_section_title '\n[.] MinIO console'
if [[ $LOCAL ]]; then
    pe 'NODE_IP=$(kubectl get nodes -o jsonpath="{.items[0].status.addresses[0].address}")'
    pe 'NODE_PORT=$(kubectl get --namespace minio-tenant -o jsonpath="{.spec.ports[0].nodePort}" services minio-console)'
    pe 'URL="https://$NODE_IP:$NODE_PORT"'
else
    pe 'export URL=https://$(kubectl get ingress -n data-wrapping glaciation-console -o jsonpath="{.spec.rules[0].host}")'
fi
pe 'echo "Serving MinIO console at $URL"'

print_section_title '\n[.] Spark history server'
if [[ $LOCAL ]]; then
    pe 'NODE_PORT=$(kubectl get --namespace spark-app -o jsonpath="{.spec.ports[0].nodePort}" services spark-history-server)'
    pe 'URL="https://$NODE_IP:$NODE_PORT"'
else
    pe 'export URL=https://$(kubectl get ingress -n spark-app data-sanitization-spark-history-server -o jsonpath="{.spec.rules[0].host}")'
fi
pe 'echo "Serving Spark history server at $URL"'

print_section_title '\n[.] Data sanitization'
if [[ $LOCAL ]]; then
    pe 'NODE_PORT=$(kubectl get --namespace spark-app -o jsonpath="{.spec.ports[0].nodePort}" services data-sanitization)'
    pe 'URL="https://$NODE_IP:$NODE_PORT"'
else
    pe 'export URL=https://$(kubectl get ingress -n spark-app data-sanitization -o jsonpath="{.spec.rules[0].host}")'
fi
pe 'echo "Serving data sanitization service at $URL"'

wait # show web interfaces

print_section_title '\n[*] Setup MinIO alias'
p 'mc alias set minio $URL $AWS_ACCESS_KEY_ID $AWS_SECRET_ACCESS_KEY'
mc alias --insecure set minio $MINIO_URL minio minio123

print_section_title '\n[*] Setup object store for the sanitization process'
p 'mc mb minio/sanitization/dataset'
mc mb --insecure minio/sanitization/dataset
p 'mc mb minio/sanitization/anonymized'
mc mb --insecure minio/sanitization/anonymized
p "mc cp ../code/spark-app/distributed/dataset/$DATASET.csv minio/sanitization/dataset/"
mc cp --insecure ../code/spark-app/distributed/dataset/$DATASET.csv minio/sanitization/dataset/

print_section_title '\n\n[*] Peak into the contents of the dataset'
p "mc head minio/sanitization/dataset/$DATASET.csv"
mc head --insecure minio/sanitization/dataset/$DATASET.csv

wait # see changes in the minio interface

print_section_title '\n[*] Run sanitization job'
pe "cat $DATASET.json"
p "curl --silent --request POST --header 'Content-Type: application/json' --data @$DATASET.json http://$NODE_IP:$NODE_PORT/api/v1alpha1/job"
OUTPUT=$(
    curl \
        --insecure \
        --silent \
        --request POST \
        --header 'Content-Type: application/json' \
        --data @$DATASET.json \
        $URL/api/v1alpha1/job
)
echo $OUTPUT
REQ_ID=$(echo $OUTPUT | jq -r .id)

print_section_title '\n[*] Waiting for the completion of the job...'
STATUS="UNKNOWN"
while [ "$STATUS" != "COMPLETED" ]; do
    if [ "$STATUS" == "FAILED" ] || [ "$STATUS" == "SUBMISSION_FAILED" ]; then
        cleanup $REQ_ID
        exit 1 # exit with an error code if the sanitization job fails
    fi

    # sleep 5
    p "curl --silent --request GET --header 'Content-Type: application/json' $URL/api/v1alpha1/job/$REQ_ID/status"
    OUTPUT=$(
        curl \
            --insecure \
            --silent \
            --request GET \
            --header 'Content-Type: application/json' \
            $URL/api/v1alpha1/job/$REQ_ID/status
    )
    echo $OUTPUT
    STATUS=$(echo $OUTPUT | jq -r .state)
    # echo "Data sanitization job with id=$REQ_ID has status=$STATUS"
done

print_section_title '\n[*] Showcase a sample of the output'
p 'mc ls minio/sanitization/anonymized'
mc ls --insecure minio/sanitization/anonymized
p "mc ls minio/sanitization/anonymized/$DATASET.csv"
mc ls --insecure minio/sanitization/anonymized/$DATASET.csv
PART=$(mc ls --insecure --json minio/sanitization/anonymized/$DATASET.csv |
       jq -r '.key | select(startswith("part-00000-")) | select(endswith(".csv"))')
p "mc head minio/sanitization/anonymized/$DATASET.csv/$PART"
mc head --insecure minio/sanitization/anonymized/$DATASET.csv/$PART

wait # see spark-app log & see the history server

cleanup $REQ_ID

wait # avoid seeing command prompt
