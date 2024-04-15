# Client service stub implementation

## 1- Service Stubs Overview

***Description:***
A Service stub implementation of the client service. This implementation is used as a preliminary placeholder for the actual implementation. This stub is build using the rust [poem](https://github.com/poem-web/poem/tree/master) framework and include an interactive OpenAPI specification.

***API Documentation:*** 
The API documentation of the service can be found [here](../docs/).

## 2- Standalone Run

Install the rust tool chain according to the documentation on [rust-lang.org](https://www.rust-lang.org/tools/install)

To start the service execute `cargo run`

Visit [http://localhost:8080/docs](http://localhost:8080/docs) for the interactive Swagger-UI documentation of the service.

### environment-variables

| variable | description | default |
| ---------|-------------|---------|
| `SERVICE_PORT` | specify the port the service will listen on | `8080` |
| `SERVICE_ADDRESS` | Address of the service | `0.0.0.0` |

## 4- Dockerization service/component

To build the service as a docker image run

`docker build -t client-service:0.1.0 .`

## 5- Helm Chart Deployment

A simple helm chart to deploy the coordination-service on kubernetes can be found at `./chart`.

### local deployment using kind

To execute and test the service locally using kind.

Create a new kind cluster using

```bash
kind create cluster --name helmtest --image kindest/node:v1.26.6
```

Now load the `client-service` image into the kind registry using 

```bash
kind load docker-image client-service:0.1.0 --name helmtest
```

Deploy the helmchart using

```bash
kubectl config use-context kind-helmtest
helm install client-service ./chart/
```
