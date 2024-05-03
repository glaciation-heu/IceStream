#!/bin/bash

set -e

S3_CLIENT="${1:-mc}"
case $S3_CLIENT in
  mc) ;;
  s3cmd) ;;
  s5cmd) ;;
  *)
    echo 'Invalid S3 client'
    exit 1
    ;;
esac

echo -e "[*] Install MinIO with Server-Side Encryption"
source install-minio-with-sse.sh ha

# Wait for the MinIO tenant services to go up
echo ''
read -n 1 -srep '<<Press any key to continue>>'

echo -e '\n[*] Interact with the MinIO tenant S3 API'
case $S3_CLIENT in
  mc)
    (
      set -x  # enable printing the command before execution (in the sub-shell)
      mc alias set myminio https://$NODE_IP:$NODE_PORT minio minio123 --insecure
      mc mb myminio/test-encrypted-bucket --insecure
      mc encrypt set sse-kms myminio-key myminio/test-encrypted-bucket --insecure
      mc ls myminio --insecure
      echo "This is a line of text" > test-object
      mc mv test-object myminio/test-encrypted-bucket --insecure
      mc ls myminio/test-encrypted-bucket --insecure
      mc cat myminio/test-encrypted-bucket/test-object --insecure
    )
    ;;
  s3cmd)
    (
      set -x  # enable printing the command before execution (in the sub-shell)
      export AWS_ACCESS_KEY=minio
      export AWS_SECRET_KEY=minio123
      s3cmd mb s3://test-encrypted-bucket --host $NODE_IP:$NODE_PORT --host-bucket $NODE_IP:$NODE_PORT --ssl --no-check-certificate
      s3cmd ls s3:// --host $NODE_IP:$NODE_PORT --host-bucket $NODE_IP:$NODE_PORT --ssl --no-check-certificate
      echo "This is a line of text" > test-object
      s3cmd put test-object s3://test-encrypted-bucket --host $NODE_IP:$NODE_PORT --host-bucket $NODE_IP:$NODE_PORT --ssl --no-check-certificate --server-side-encryption --server-side-encryption-kms-id myminio-key
      s3cmd ls s3://test-encrypted-bucket --host $NODE_IP:$NODE_PORT --host-bucket $NODE_IP:$NODE_PORT --ssl --no-check-certificate
      s3cmd get s3://test-encrypted-bucket/test-object --host $NODE_IP:$NODE_PORT --host-bucket $NODE_IP:$NODE_PORT --ssl --no-check-certificate - | cat
    )
    ;;
  s5cmd)
    (
      set -x  # enable printing the command before execution (in the sub-shell)
      export AWS_ACCESS_KEY=minio
      export AWS_SECRET_KEY=minio123
      export S3_ENDPOINT_URL=https://$NODE_IP:$NODE_PORT
      s5cmd --no-verify-ssl mb s3://test-encrypted-bucket
      s5cmd --no-verify-ssl ls
      echo "This is a line of text" > test-object
      s5cmd --no-verify-ssl mv --sse aws:kms --sse-kms-key-id myminio-key test-object s3://test-encrypted-bucket
      s5cmd --no-verify-ssl ls s3://test-encrypted-bucket
      s5cmd --no-verify-ssl cat s3://test-encrypted-bucket/test-object
    )
    ;;
esac

# Wait before deletion
echo ''
read -n 1 -srep '<<Press any key to continue>>'

echo -e "\n[*] Uninstall HashiCorp Vault"
helm uninstall --namespace vault vault

echo -e "\n[*] Uninstall cert-manager"
helm uninstall --namespace cert-manager cert-manager

echo -e "\n[*] Uninstall replicator"
helm uninstall --namespace replicator kubernetes-replicator

echo -e '\n[*] Uninstall MinIO operator'
helm uninstall --namespace minio-operator operator

rm -r $WORKDIR
