# Live analytics at edge computation

This services facilitates the execution of code (specifically code for analytics)
on edge device. For example, UC2 will deploy this on the 5200 gateways.

## Overview

Processing at the edge is one of the most important locations for processing
within the GLACIATION platform. For example, in a manufacturing setting, processing
will take place on edge devices. There is a significant chance this processing
will be on video which is not data that we want to either store at the edge
or move within the platform.

## Service Dependencies

This service leverages WasmEdge for processing at the edge. Therefore, it is
expected the service will either carry out wasm compilation or accept
wasm files for analytics.

![Image displaying the architecture of the service](docs/architecture.png)