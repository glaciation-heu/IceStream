# Secure Collaborative Computation

The Secure Collaborative Computation consists of two main services for cryptographic protection via secure multi-party computation (MPC), i.e., Computation Service and Client Service. It also considers an optional visualization service to provide utility-accuracy feedback for privacy protection, i.e., differential privacy (DP).

* [Computation Service](compute_service/docs/README.md) runs the distributed MPC computation on encrypted data.

* [Client Service](client_service/docs/README.md) provides encrypted input for the Computation Service.

* [DP Visualization Service](dp_visualization/docs/README.md) visualized utility-accuracy trade-offs for differential privacy parameterization (as stand-alone component to foster data sharing or in case MPC program computes DP mechanism).


## Terminology
Next, we centrally overview basic parameters, concepts, and terminology used in the components and/or their descriptions.

#### Basic Parameters
| Parameter | Description |
| --------- | ----------- |
|`collaboration_id`| Identifier for a secure MPC collaboration project|
|`party_id` | identifier for a specific party |
|`secret_id` | identifier for an input (the same for every share of the input on different Computation Parties) |
|`secret_tags` | tags specified by the user to identify a secret |
|`program_name` | Name of a secure computation program |
|`program_params` | Parameters for a secure computation program, e.g. accuracy-performance trade-off for approximations |
|`cs_config` | Computation Service configuration. Defined by [CarbyneStack](https://carbynestack.io/getting-started/cli/#prerequisites)

#### Basic Concepts & Overview
*MPC:*
* Secure Multi-Party Computation (MPC): computation on encrypted data with multiples parties (Input, Computation, Output Parties)
* Input Parties: parties (identified via `party_id`) which provides the input (identified via `secret_id`) for a secure computation via Client Service
* Computation Parties: parties that executes the secure computation (realized as abstraction via Computation Service)
* Output Parties: parties that receives the output of a secure computation (currently, no separate entities, e.g., input party and/or Coordinator can learn result)
* Secure Computation Program (MPC program): set of instructions to perform a secure computation (identified via `program_name`)

*Collaborations:*
* Collaborations (identified via `collaboration_id`) are pre-defined in Coordination Service (e.g., based on pre-defined MPC programs identified via program_name to be run in the computation)
* Participants (i.e., Input Parties identified via `party_id`) can register for participation at Coordination Service (available collaboration_ids assumed to be known for now)

*Collaboration start*: Coordination Service has some internal rule associated with a collaboration (say, minimum number of required parties provided input in a fixed time frame)