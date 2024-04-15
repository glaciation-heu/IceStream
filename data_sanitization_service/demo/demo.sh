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

echo '[*] Configure object store for the sanitization process'
(
    set -x
    mc mb --insecure myminio/sanitization/dataset
    mc mb --insecure myminio/sanitization/anonymized
    mc cp --insecure ../code/spark-app/distributed/dataset/$DATASET.csv myminio/sanitization/dataset/
)

echo -e '\n\n[*] Peak into the contents of the dataset'
(set -x; mc head --insecure myminio/sanitization/dataset/$DATASET.csv)

NODE_IP=$(kubectl get nodes --namespace spark-app -o jsonpath="{.items[0].status.addresses[0].address}")
NODE_PORT=$(kubectl get --namespace spark-app -o jsonpath="{.spec.ports[0].nodePort}" services data-sanitization)

echo -e '\n[*] Run sanitization job'
REQ_ID=$(
    curl \
        --silent \
        --request POST \
        --header 'Content-Type: application/json' \
        --data @$DATASET.json \
        http://$NODE_IP:$NODE_PORT/api/v1alpha1/job | jq -r .id
)

echo -e '\nWaiting for the completion of the sanitization job...'
STATUS="UNKNOWN"
while [ "$STATUS" != "COMPLETED" ]; do
    sleep 5
    STATUS=$(
        curl \
            --silent \
            --request GET \
            --header 'Content-Type: application/json' \
            http://$NODE_IP:$NODE_PORT/api/v1alpha1/job/$REQ_ID/status | jq -r .state
    )
    echo "Data sanitization job with id=$REQ_ID has status=$STATUS"
done

echo -e '\n[*] Showcase a sample of the output'
(
    set -x # enable printing the command before execution (in the sub-shell)
    mc ls --insecure myminio/sanitization/anonymized
    mc ls --insecure myminio/sanitization/anonymized/$DATASET.csv
)
PART=$(mc ls --insecure --json myminio/sanitization/anonymized/$DATASET.csv |
       jq -r '.key | select(startswith("part-00000-")) | select(endswith(".csv"))')
(set -x; mc head --insecure myminio/sanitization/anonymized/$DATASET.csv/$PART)

# Wait before deletion
echo ''
read -n 1 -srep '<<Press any key to continue>>'

echo -e '\n[*] Delete sanitization job'
curl \
    --silent \
    --request DELETE \
    --header 'Content-Type: application/json' \
    --output /dev/null \
    http://$NODE_IP:$NODE_PORT/api/v1alpha1/job/$REQ_ID
