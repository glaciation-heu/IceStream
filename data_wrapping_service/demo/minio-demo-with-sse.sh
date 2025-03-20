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

if [[ $INSTALL ]]; then
  echo -e "[*] Install MinIO with Server-Side Encryption"
  source install-minio-with-sse.sh ha

  # Wait for the MinIO tenant services to go up
  echo ''
  read -n 1 -srep '<<Press any key to continue>>'
fi

if [[ $LOCAL ]]; then
  HOST=$NODE_IP:$NODE_PORT
else
  HOST=$(kubectl get ingress -n data-wrapping glaciation -o jsonpath="{.spec.rules[0].host}")
fi

echo -e '\n[*] Interact with the MinIO tenant S3 API'
case $S3_CLIENT in
  mc)
    (
      set -x  # enable printing the command before execution (in the sub-shell)
      mc alias set minio https://$HOST minio minio123 --insecure
      mc mb minio/test-encrypted-bucket --ignore-existing --insecure
      mc encrypt set sse-kms encryption-key minio/test-encrypted-bucket --insecure
      mc ls minio --insecure
      echo "This is a line of text" > test-object
      mc mv test-object minio/test-encrypted-bucket --insecure
      mc ls minio/test-encrypted-bucket --insecure
      mc cat minio/test-encrypted-bucket/test-object --insecure
    )
    ;;
  s3cmd)
    (
      set -x  # enable printing the command before execution (in the sub-shell)
      export AWS_ACCESS_KEY=minio
      export AWS_SECRET_KEY=minio123
      s3cmd mb s3://test-encrypted-bucket --host $HOST --host-bucket $HOST --ssl --no-check-certificate
      s3cmd ls s3:// --host $HOST --host-bucket $HOST --ssl --no-check-certificate
      echo "This is a line of text" > test-object
      s3cmd put test-object s3://test-encrypted-bucket --host $HOST --host-bucket $HOST --ssl --no-check-certificate --server-side-encryption --server-side-encryption-kms-id encryption-key
      s3cmd ls s3://test-encrypted-bucket --host $HOST --host-bucket $HOST --ssl --no-check-certificate
      s3cmd get s3://test-encrypted-bucket/test-object --host $HOST --host-bucket $HOST --ssl --no-check-certificate - | cat
    )
    ;;
  s5cmd)
    (
      set -x  # enable printing the command before execution (in the sub-shell)
      export AWS_ACCESS_KEY=minio
      export AWS_SECRET_KEY=minio123
      export S3_ENDPOINT_URL=https://$HOST
      s5cmd --no-verify-ssl mb s3://test-encrypted-bucket
      s5cmd --no-verify-ssl ls
      echo "This is a line of text" > test-object
      s5cmd --no-verify-ssl mv --sse aws:kms --sse-kms-key-id encryption-key test-object s3://test-encrypted-bucket
      s5cmd --no-verify-ssl ls s3://test-encrypted-bucket
      s5cmd --no-verify-ssl cat s3://test-encrypted-bucket/test-object
    )
    ;;
esac

if [[ $INSTALL ]]; then
  # Wait before deletion
  echo ''
  read -n 1 -srep '<<Press any key to continue>>'

  echo -e "\n[*] Uninstall HashiCorp Vault"
  helm uninstall --namespace vault vault

  echo -e "\n[*] Uninstall trust-manager"
  helm uninstall --namespace cert-manager trust-manager

  echo -e "\n[*] Uninstall cert-manager"
  helm uninstall --namespace cert-manager cert-manager

  echo -e '\n[*] Uninstall MinIO operator'
  helm uninstall --namespace minio-operator operator

  rm -r $WORKDIR
fi
