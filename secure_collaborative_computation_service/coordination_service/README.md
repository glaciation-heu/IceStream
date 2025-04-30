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

## Interaction between compute, client, coordination service and parties
Next, an overview of communication between the three services and parties is given.
We assume the following:
* Computation Service is running
* Coordination Service has the configuration (config) for the Computation Service (i.e., IP addresses of Carbyne Stack instances)

The Input Party (IP) provides data to a collaboration, the Output Party (OP) receives the computed results of the collaboration.
There can be multiple Input and Output Parties and each runs its own Client Service.

```mermaid
sequenceDiagram
    #define order
    actor Input Party
    participant Client Service (IP)
    participant Coordinator
    participant Computation Services
    participant Client Service (OP)
    actor Output Party

    Output Party ->> +Coordinator: POST /collaboration (create new collaboration)
    Coordinator --) -Output Party: Collaboration ID (CID)

    Output Party ->> + Coordinator: PUT /collaboration/<CID>/register-output-party/<Party ID (PID)>
    Coordinator --) - Output Party: successfully registered

    Input Party ->> +Coordinator: PUT /collaboration/<CID>/register-input-party/<PID>
    activate Input Party
    Coordinator --) -Input Party: OK, input-data specification (csv header + row count)

    Input Party ->> Client Service (IP): POST /secrets/<CID>/<PID>

    deactivate Input Party
    activate Client Service (IP)
    Client Service (IP) ->> +Computation Services: GET /input-masks
    Computation Services --) -Client Service (IP): masks used to securely share secret shares
    Client Service (IP) ->> +Client Service (IP): Create secret shares
    Client Service (IP) --) -Client Service (IP): Shares + Secret IDs (SIDs)

    Client Service (IP) ->> +Coordinator: GET /collaboration/<CID>/compute-config
    Coordinator --) -Client Service (IP): config used to upload secret shares
    
    Client Service (IP) ->> +Computation Services: POST /amphora/masked-inputs (upload secret shares)
    Computation Services --) -Client Service (IP): OK
    Client Service (IP) ->> Coordinator: PUT /confirm-upload/<CID>/<PID> request-body: <SIDs>
    activate Coordinator
    Coordinator --) Client Service (IP): OK
    deactivate Client Service (IP)
    
    alt ready to start collaboration
        Coordinator ->> +Computation Services: POST /ephemeral (start computation)
        Computation Services --) -Coordinator: result SID
        
        Coordinator ->> Client Service (OP): PUT /notify/<CID> request-body: <result SID>
        deactivate Coordinator
        activate Client Service (OP)
        Client Service (OP) ->> +Computation Services: GET /amphora/secret-shares/<result SID> (get result)
        Computation Services --) -Client Service (OP): results
        
        Client Service (OP) --) Output Party: results
        deactivate Client Service (OP)
    end
```

### In text format

In this example the output party acts as the initiator and creates a new collaboration on the coordinator. The collaboration contains the MPC program and input data specification for it. The output party then registers for a collaboration providing the endpoints of its client service to the coordinator.

The input party registers for a collaboration. The coordinator returns the specification for the input data.

Afterword the input party uploads the data for the collaboration to its client service. The client service calculates the secret shares from the data and distributes the shares to the different computation services. To find the computation services the client service requests the compute-service-configuration from the coordinator. Lastly the client service notifies the coordinator that the data was successfully uploaded to the computation services and provides the ids of the crated secrets.

If the collaboration is ready to be executed (e.g. all input parties have uploaded the data) the coordinator starts the calculation of the mpc program. After the computation is finished the coordinator notifies the client service of the output party which is now able to get the results from the computation service.

## 4-REST API
The Rest-API is described by the provided [OpenAPI](openapi.yml) specification.

## 5-Stub
A service stub is defined in [stub](../stub/README.md).
