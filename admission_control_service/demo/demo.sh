#!/bin/bash

function print_and_create_resource {
    if [ $# -eq 2 ]; then
        echo -e "\n$1"
    fi
    curl -s ${@: -1} | sed -e 's/^/> /'
    kubectl create -f ${@: -1}
}

# By setting the KUBECONFIG environment variable it is possible to run the demo
# against different kubernetes environments

echo '[*] Install admission control service'
helm repo add gatekeeper https://open-policy-agent.github.io/gatekeeper/charts
helm install gatekeeper/gatekeeper --name-template=gatekeeper --namespace gatekeeper-system --create-namespace

echo -e '\nWaiting for the rollout of the service...'
kubectl -n gatekeeper-system rollout status deploy/gatekeeper-audit
kubectl -n gatekeeper-system rollout status deploy/gatekeeper-controller-manager

echo -e '\n[*] Install admission control web UI'
helm repo add gpm https://sighupio.github.io/gatekeeper-policy-manager
helm upgrade --install --namespace gatekeeper-system --set image.tag=v1.0.10 --values values.yaml gatekeeper-policy-manager gpm/gatekeeper-policy-manager

echo -e '\nWaiting for the rollout of the service...'
kubectl -n gatekeeper-system rollout status deploy/gatekeeper-policy-manager

export NODE_PORT=$(kubectl get --namespace gatekeeper-system -o jsonpath="{.spec.ports[0].nodePort}" services gatekeeper-policy-manager)
export NODE_IP=$(kubectl get nodes --namespace gatekeeper-system -o jsonpath="{.items[0].status.addresses[0].address}")
echo -e "\nServing Gatekeeper Policy Manager at http://$NODE_IP:$NODE_PORT"

echo -e '\n[*] Add constraint template'
print_and_create_resource 'https://raw.githubusercontent.com/open-policy-agent/gatekeeper-library/master/library/general/allowedrepos/template.yaml'

echo -e '\n[*] Add constraint'
print_and_create_resource 'https://raw.githubusercontent.com/open-policy-agent/gatekeeper-library/master/library/general/allowedrepos/samples/repo-must-be-openpolicyagent/constraint.yaml'

echo -e '\n[*] Test'
print_and_create_resource 'Deploy pod with Open Policy Agent container' 'https://raw.githubusercontent.com/open-policy-agent/gatekeeper-library/master/library/general/allowedrepos/samples/repo-must-be-openpolicyagent/example_allowed.yaml'
print_and_create_resource 'Deploy pod with NGINX container' 'https://raw.githubusercontent.com/open-policy-agent/gatekeeper-library/master/library/general/allowedrepos/samples/repo-must-be-openpolicyagent/example_disallowed_container.yaml'
print_and_create_resource 'Deploy pod with NGINX init container and Open Policy Agent container' 'https://raw.githubusercontent.com/open-policy-agent/gatekeeper-library/master/library/general/allowedrepos/samples/repo-must-be-openpolicyagent/example_disallowed_initcontainer.yaml'
print_and_create_resource 'Deploy pod with NGINX init container and NGINX container' 'https://raw.githubusercontent.com/open-policy-agent/gatekeeper-library/master/library/general/allowedrepos/samples/repo-must-be-openpolicyagent/example_disallowed_both.yaml'

echo -e '\n[*] Test clean-up'
kubectl delete -f https://raw.githubusercontent.com/open-policy-agent/gatekeeper-library/master/library/general/allowedrepos/samples/repo-must-be-openpolicyagent/example_allowed.yaml
kubectl delete -f https://raw.githubusercontent.com/open-policy-agent/gatekeeper-library/master/library/general/allowedrepos/samples/repo-must-be-openpolicyagent/example_disallowed_container.yaml
kubectl delete -f https://raw.githubusercontent.com/open-policy-agent/gatekeeper-library/master/library/general/allowedrepos/samples/repo-must-be-openpolicyagent/example_disallowed_initcontainer.yaml
kubectl delete -f https://raw.githubusercontent.com/open-policy-agent/gatekeeper-library/master/library/general/allowedrepos/samples/repo-must-be-openpolicyagent/example_disallowed_both.yaml

echo -e '\n[*] Uninstall admission control web UI'
helm delete gatekeeper-policy-manager --namespace gatekeeper-system

echo -e '\n[*] Uninstall admission control service'
helm delete gatekeeper --namespace gatekeeper-system
kubectl delete crd -l gatekeeper.sh/system=yes
