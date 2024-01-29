# Component Overview:
- **Description**: Distributed Knowledge Graph refers to the Novel Metadata Fabric of the GLACIATION platform, contains 7 components as follows:
- **Objectives**: 6 other microservices will be developed and provide REST API following OpenAPI specifications.
* [Jena component](jena/)
* [Metadata Service](metadata_service/)
* [Prediction service](prediction_service/)
* [Replica Service](replica_service/)
* [Trade-off Service](trade_off_service/)
* [Data Storage Service](data_storage_service/)
* [Data Processing and Monitoring Service](data_processing_monitoring_service/)

# Service Dependencies:
For each component, there will be separate ```.md``` file under the ```docs``` folder of each service describing its dependencies.

# Service Architecture:
- Jena Fuseki instance will be used as DB for storing DKG. DeamonSet in K8S cluster​, 1 for each node, 5 in total​ in Dell setting.
- Other microservices can be deployment or Replicaset​
- For each component, there will be separate ```.md``` file under the ```docs``` folder of each service describing its architecture respectively.




