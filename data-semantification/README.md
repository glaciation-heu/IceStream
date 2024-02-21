# Data Semantification Service

This services provides the primary entrypoint for data submission to the
GLACIATION platform.

## Overview

When raw data, e.g., csv or video, is submitted to the GLACIATION platform
it needs semantification. This means the transformation from raw data
to linked data. Linked data then can be either split into data/metadata
or stored within the DKG.

The goals of the service is to transform the input raw data to
Linked data or Linked metadata such that it can be stored in the DKG

## Dependencies

To use the service you must supply a NiFi Flow Controller (with Connections).
Furthermore, the JOLT (JsOn Language for Transform) must be embedded
in the Flow Controller.

## Architecture

![Image displaying the architecture of the service](docs/architecture.png)

Further details about [NIFI](https://nifi.apache.org/) and [JOLT](https://github.com/bazaarvoice/jolt)
