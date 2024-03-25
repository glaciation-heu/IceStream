# Secure Collaborative Computation

The Secure Collaborative Computation consists of two main services for cryptographic protection via secure multi-party computation (MPC), i.e., Computation Service and Client Service. It also considers an optional visualization service to provide utility-privacy feedback for privacy protection via anonymization, i.e., differential privacy (DP).

In the context of UC3, MPC protects collaborative computations on distributed data (computation on encrypted data) and DP-Viz helps to parameterize DP-based anonymization (anonymized data sharing). Potentially, DP mechanisms can be implemented in MPC, i.e., computations on encrypted data with anonymized results, where DP-Viz provides guidance for initial DP paramterization (accuracy-privacy feedback).

* [Computation Service](compute_service/docs/README.md) runs the distributed MPC computation on encrypted data. (Separate "platform" independent from Glaciation.)

* [Client Service](client_service/docs/README.md) provides encrypted input for the Computation Service. (Interface for Glaciation to Computation Service, takes data from Glaciation or a trusted domain, e.g., edge, on-prem, encrypts it and uploads encrypted data to Computation Service for computation on encrypted data.)

* [DP Visualization Service](dp_visualization/docs/README.md) visualized utility-accuracy trade-offs for differential privacy parameterization. (To foster anonymized data sharing.)
