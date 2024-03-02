# Jena component

Brief description of your project.

## Table of Contents

- [Overview](#overview)
- [Using jena-daemonset.yaml](#using-jena-daemonsetyaml)

## Overview

TBD

## Using jena-daemonset.yaml

`jena-daemonset.yaml` is a configuration file for deploying Jena as a DaemonSet on a Kubernetes cluster.

### Prerequisites

- Ensure you have `kubectl` installed and configured to communicate with your Kubernetes cluster.

### Deployment

To deploy Jena using the `jena-daemonset.yaml`, follow the steps below:

   1. Navigate to the directory containing `jena-daemonset.yaml`.
      ```bash
      cd /path/to/directory
      ```

   2. Deploy the DaemonSet:
      ```bash
      kubectl apply -f jena-daemonset.yaml
      ```

   3. Monitor the DaemonSet rollout:
      ```bash
      kubectl rollout status daemonset/jena-daemonset
      ```

### Accessing Jena

TBD

### Troubleshooting

TBD

