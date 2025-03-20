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

clear
wait # avoid seeing command prompt

if [[ $INSTALL ]]; then
  echo -e "[*] Install MinIO with Server-Side Encryption"
  source install-minio-with-sse.sh ha

  # Wait for the MinIO tenant services to go up
  echo ''
  read -n 1 -srep '<<Press any key to continue>>'
fi

print_section_title "[*] Let's see what is running in the Kubernetes cluster"
pe 'kubectl get pods --namespace data-wrapping'

print_section_title '\n[*] External services'
print_section_title '\n[.] MinIO'
if [[ $LOCAL ]]; then
  pe 'HOST=$NODE_IP:$NODE_PORT'
else
  pe 'HOST=$(kubectl get ingress -n data-wrapping glaciation -o jsonpath="{.spec.rules[0].host}")'
fi
pe 'echo "Serving MinIO at https://$HOST"'

print_section_title '\n[.] MinIO console'
if [[ $LOCAL ]]; then
    pe 'NODE_IP=$(kubectl get nodes -o jsonpath="{.items[0].status.addresses[0].address}")'
    pe 'NODE_PORT=$(kubectl get --namespace minio-tenant -o jsonpath="{.spec.ports[0].nodePort}" services minio-console)'
    pe 'URL=https://$NODE_IP:$NODE_PORT'
else
    pe 'URL=https://$(kubectl get ingress -n data-wrapping glaciation-console -o jsonpath="{.spec.rules[0].host}")'
fi
pe 'echo "Serving MinIO console at $URL"'
pe 'AWS_ACCESS_KEY=minio'
pe 'AWS_SECRET_KEY=minio123'
pe 'echo "User: $AWS_ACCESS_KEY"'
pe 'echo "Password: $AWS_SECRET_KEY"'

print_section_title '\n[.] Vault'
if [[ $LOCAL ]]; then
    pe 'NODE_IP=$(kubectl get nodes -o jsonpath="{.items[0].status.addresses[0].address}")'
    pe 'NODE_PORT=$(kubectl get --namespace minio-tenant -o jsonpath="{.spec.ports[0].nodePort}" services data-wrapping-vault)'
    pe 'URL=https://$NODE_IP:$NODE_PORT'
else
    pe 'URL=https://$(kubectl get ingress -n data-wrapping data-wrapping-vault -o jsonpath="{.spec.rules[0].host}")'
fi
pe 'echo "Serving Vault at $URL"'
pe 'POD_NAME=$(kubectl get pod --namespace data-wrapping --selector app=auto-unseal-vault-cluster -o jsonpath="{.items[0].metadata.name}")'
pe 'VAULT_ROOT_TOKEN=$(kubectl exec -it --namespace data-wrapping $POD_NAME --container vault -- cat /vault/unseal/response.json | jq -r ".root_token")'
pe 'echo "Token: $VAULT_ROOT_TOKEN"'


print_section_title '\n[*] Interact with the MinIO tenant S3 API'
case $S3_CLIENT in
  mc)
    (
      p 'mc alias set minio https://$HOST $AWS_ACCESS_KEY $AWS_SECRET_KEY'
      mc alias set minio https://$HOST minio minio123 --insecure
      p 'mc mb minio/test-encrypted-bucket --ignore-existing'
      mc mb minio/test-encrypted-bucket --ignore-existing --insecure
      p 'mc encrypt set sse-kms encryption-key minio/test-encrypted-bucket'
      mc encrypt set sse-kms encryption-key minio/test-encrypted-bucket --insecure
      p 'mc ls minio'
      mc ls minio --insecure
      pe 'echo "This is a line of text" > test-object'
      p 'mc mv test-object minio/test-encrypted-bucket'
      mc mv test-object minio/test-encrypted-bucket --insecure
      p 'mc ls minio/test-encrypted-bucket'
      mc ls minio/test-encrypted-bucket --insecure
      p 'mc cat minio/test-encrypted-bucket/test-object'
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

wait # avoid seeing command prompt
