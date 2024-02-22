# Coordination Service

## 1-Component Overview
***Description:***
The coordination service coordinates different client services for collaborative scenarios as well as the computation service.

***Objective:***
The idea is to have a central point to facilitate coordination.
Allowing clients to find collaborations, start the MPC execution when sufficient inputs are available, and inform them when results are available.

## 2-Service Dependencies
***External Dependencies:***
This service realizes a REST-API using the [poem](https://github.com/poem-web/poem/tree/master) framework.

***Internal Dependencies:***
The component itself requires a form of database to keep track of collaborations.

## 3-Service Architecture

***Hight-Level Architecture:***

![diagram image](images/coordination_service_overview.png)

Mainly, the coordination service allows clients to find collaborations, register participation and provided inputs, starts the MPC execution, and informs clients when results are available.

```mermaid
sequenceDiagram
    #define order
    participant Client Service
    participant Coordinator
    participant Computation Service

    Client Service->>Coordinator: register participation
    activate Coordinator

    Coordinator->>Client Service: ready for input
    deactivate Coordinator
    Client Service->>Computation Service: encrypted input
    activate Client Service

    Client Service->>Coordinator: register input
    deactivate Client Service
    activate Coordinator

    Coordinator->>Computation Service: start MPC
    #Computation Service--)Coordinator: #
    loop until result is ready
        Coordinator->>Computation Service: Check result ready
    end

    Coordinator--)Client Service: result ready
    deactivate Coordinator
    activate Client Service
    Client Service->>Computation Service: get result
    Computation Service--)Client Service: encrypted result
    Client Service->>Coordinator: Finished
    deactivate Client Service
```

## 4-REST API
The Rest-API is described by the provided [OpenAPI](openapi.yml) specification.