# Admission Control Service

This service validates the creation, modification and deletion of Kubernetes
resources within the Kubernetes cluster with the goal of meeting governance
and legal requirements, but also ensuring adherence to best practices and
institutional conventions.

## Overview

Kubernetes allows decoupling policy decisions from the inner workings of the
API server by means of admission controller webhooks, which are executed
whenever a resource is created, updated or deleted. This service provides
mutating and validating webhook that modify objects sent to the API server to
enforce custom defaults, or reject requests to enforce custom policies.
