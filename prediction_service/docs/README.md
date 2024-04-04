# Service Overview:
- Description: Provide forecasting functionality with high-granularity time series data.
- Objectives: Provide energy consumption prediction for the next day/month.

# Service Dependencies:
- External Dependencies: Performance measurement framework to get raw data based on metadata about this datasource from Metadata microservice. The metadata information of the performance metrics might be donw via Data Processing and Monitoring microservice.
- Internal Dependencies: Metadata microservice for read. Data Storage Service to store the prediction history. 

# Service Architecture:
![](v20240205.JPG) 
- [Kubernetes Batch Job](https://hevodata.com/learn/kubernetes-batch-job/#:~:text=What%20is%20Kubernetes%20Batch%20Job%3F,-Image%20Source&text=A%20job%20creates%20one%20or,pod%20completions%20as%20they%20happen.)

# Contact:
DELL Technologies (Guangyuan.Piao@dell.com)

# Todo list
- [x] Service description
- [x] OpenAPI specification
- [ ] Batch job for prediction
- [ ] Connect to DSS service
- [ ] Connect to metadata service
