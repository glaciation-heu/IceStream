# Service Overview:
- Description: Store access patterns about data sources, and write daily summary statistics to DKG for the last n days.
- Objectives: Keep track of how many times a data source has been queried in SPARQL requests.

# Service Dependencies:
- External Dependencies: N/A
- Internal Dependencies: Metadata microservice to write back a summary statistics for n days.

# Service Architecture:
![](data-storage-service-v20240206.JPG) 

# Contact
DELL Technologies (Guangyuan.Piao@dell.com)

# Todo list
- [x] Service description
- [ ] OpenAPI specification
- [ ] REST API implementation
- [ ] Batch job implemetation, connect to metadata service
