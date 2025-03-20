#!/bin/bash

. demo-magic.sh -n -w3

function print_section_title {
    echo -n $'\e[32;1m'
    echo -e "$1"
    echo -n $'\e[0m'
}

function print_and_create_resource {
    if [ $# -eq 2 ]; then
        echo -e "\n$1"
    fi
    pe "cat ${@: -1}"
    pe "kubectl create -f ${@: -1}"
}

# By setting the KUBECONFIG environment variable it is possible to run the demo
# against different kubernetes environments

clear
wait # avoid seeing command prompt

if [[ $INSTALL ]]; then
    print_section_title '[*] Install admission control service'
    pe 'helm repo add gatekeeper https://open-policy-agent.github.io/gatekeeper/charts'
    pe 'helm install gatekeeper/gatekeeper --name-template=gatekeeper --namespace gatekeeper-system --create-namespace'

    # Waiting for the rollout of the service
    pe 'kubectl -n gatekeeper-system rollout status deploy/gatekeeper-audit'
    pe 'kubectl -n gatekeeper-system rollout status deploy/gatekeeper-controller-manager'

    print_section_title '\n[*] Install admission control web UI'
    pe 'helm repo add gpm https://sighupio.github.io/gatekeeper-policy-manager'
    pe 'helm upgrade --install --namespace gatekeeper-system --set image.tag=v1.0.10 --values values.yaml gatekeeper-policy-manager gpm/gatekeeper-policy-manager'
    echo ''

    # Waiting for the rollout of the service
    pe 'kubectl -n gatekeeper-system rollout status deploy/gatekeeper-policy-manager'
    echo ''
fi

print_section_title "[*] Let's see what is running in our Kubernetes cluster"
pe 'kubectl get pods --namespace gatekeeper-system'

print_section_title '\n[*] External services'
print_section_title '\n[.] Gatekeeper Policy Manager'
if [[ $LOCAL ]]; then
    pe 'export NODE_PORT=$(kubectl get --namespace gatekeeper-system -o jsonpath="{.spec.ports[0].nodePort}" services gatekeeper-policy-manager)'
    pe 'export NODE_IP=$(kubectl get nodes --namespace gatekeeper-system -o jsonpath="{.items[0].status.addresses[0].address}")'
    pe 'export URL=http://$NODE_IP:$NODE_PORT)'
else
    pe 'export URL=http://$(kubectl get ingress -n gatekeeper-system gatekeeper-policy-manager -o jsonpath="{.spec.rules[0].host}")'
fi
pe 'echo "Serving Gatekeeper Policy Manager at $URL"'

print_section_title '\n[*] Add constraint template'
print_and_create_resource '../policy-library/library/general/allowedrepos/template.yaml'
wait # show constraint template in the web UI

print_section_title '\n[*] Add constraint'
print_and_create_resource '../policy-library/library/general/allowedrepos/samples/repo-must-be-openpolicyagent/constraint.yaml'
wait # show constraint in the web UI

print_section_title '\n[*] Test'
print_and_create_resource 'Deploy pod with Open Policy Agent container' '../policy-library/library/general/allowedrepos/samples/repo-must-be-openpolicyagent/example_allowed.yaml'
wait # explain test
print_and_create_resource 'Deploy pod with NGINX container' '../policy-library/library/general/allowedrepos/samples/repo-must-be-openpolicyagent/example_disallowed_container.yaml'
wait # explain test
print_and_create_resource 'Deploy pod with NGINX init container and Open Policy Agent container' '../policy-library/library/general/allowedrepos/samples/repo-must-be-openpolicyagent/example_disallowed_initcontainer.yaml'
wait # explain test
print_and_create_resource 'Deploy pod with NGINX init container and NGINX container' '../policy-library/library/general/allowedrepos/samples/repo-must-be-openpolicyagent/example_disallowed_both.yaml'
wait # explain test

print_section_title '\n[*] Test clean-up'
pe 'kubectl delete -f ../policy-library/library/general/allowedrepos/samples/repo-must-be-openpolicyagent/example_allowed.yaml'
pe 'kubectl delete -f ../policy-library/library/general/allowedrepos/samples/repo-must-be-openpolicyagent/example_disallowed_container.yaml'
pe 'kubectl delete -f ../policy-library/library/general/allowedrepos/samples/repo-must-be-openpolicyagent/example_disallowed_initcontainer.yaml'
pe 'kubectl delete -f ../policy-library/library/general/allowedrepos/samples/repo-must-be-openpolicyagent/example_disallowed_both.yaml'
pe 'kubectl delete -f ../policy-library/library/general/allowedrepos/samples/repo-must-be-openpolicyagent/constraint.yaml'
pe 'kubectl delete -f ../policy-library/library/general/allowedrepos/template.yaml'

if [[ $INSTALL ]]; then
    print_section_title '\n[*] Uninstall admission control web UI'
    pe 'helm delete gatekeeper-policy-manager --namespace gatekeeper-system'

    print_section_title '\n[*] Uninstall admission control service'
    pe 'helm delete gatekeeper --namespace gatekeeper-system'
    pe 'kubectl delete crd -l gatekeeper.sh/system=yes'
fi

wait # avoid seeing command prompt
