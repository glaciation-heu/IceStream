The following describes the way included scripts work. 

# Time Series Generator


## Desciption
This script contains classes, functions and configuration files for generation and manipulation of synthetic timeseries data related to a k83 cluter.


## Running the Script

You can run the script from the command line as follows:

1- Make your desired changes in `timeseries_generator/configurations`  
2- Change directory to `time_series_generator`

```bash
python timeseries_generator.py
```

Accompanied with this scrip there there is dockerised version of the generator with an API accessible on port 8080 of the container. 

Once inside the /docker directory
```
 docker build -t generator .
````

And the launch the container
```
docker run -p 5005:8080 generator
```

Query the API for the metrics:  
- http://127.0.0.1:5005/display # for viewing the data  
- http://127.0.0.1:5005/download # for downloading the data as csv file

## Components:
- Power consumption calculator # expressions are rough estimation and can vary with real world usage functions

- Workload class expressions # expressions are rough estimation and may not represented real-world workload classes

- Container with Flask API to serve the generated data


## Functions

### deep_merge_dicts(dict1, dict2)

This function merges two dictionaries deeply. If the same key exists in both dictionaries and the values are also dictionaries, it merges those dictionaries as well.

#### Parameters

- `dict1` : The first dictionary to merge.
- `dict2` : The second dictionary to merge.

#### Returns

- The merged dictionary.

### merge_yaml_files(config_file)

This function merges multiple YAML files into one. It takes the path of a YAML file as input, which contains the paths of other YAML files to be included in the 'includes' section. The function returns the merged data if 'includes' section is present, else it returns the input file path.

#### Parameters

- `config_file` : The path of the YAML file.

#### Returns

- The merged data from all the included YAML files or the input file path.

## Classes

### HardwareMetric

This class represents a hardware metric. It has an `income_function` attribute which is used to calculate the value of the metric.

### WLClass

This is a base class for workload classes. It has several attributes like `name`, `lifespan`, `noise_factor`, `variation_range`, `description`, `expression`, `noise_mean`, `noise_std_dev`, and `hardware_metrics`.


## Workload classes

### BatchProcessing

This class inherits from `WLClass` and represents a batch processing workload. It overrides the `get_expression` and `apply_expression` methods from the base class.

### OLTP

This class inherits from `WLClass` and represents an OLTP (Online Transaction Processing) workload. It overrides the `get_expression` and `apply_expression` methods from the base class.

### ECommerce

This class inherits from `WLClass` and represents an E-commerce workload. It overrides the `get_expression` and `apply_expression` methods from the base class.

### DataAnalytics

This class inherits from `WLClass` and represents a data analytics workload. It overrides the `get_expression` and `apply_expression` methods from the base class.

### ScientificComputing

This class inherits from `WLClass` and represents a scientific computing workload. It overrides the `apply_expression` method from the base class.

### WebServing

This class inherits from `WLClass` and represents a web serving workload. It overrides the `get_expression` and `apply_expression` methods from the base class.

## Generator

This class is responsible for generating instances of different workload classes based on the configuration.

## Workload

This class represents a workload. It has several attributes like `workload_id`, `workload_pod_id`, `wlClass`, and `metrics`.

### process_config()

This function processes the configuration and creates a `Generator` instance.

### create_workloads()

This function creates workloads based on the provided generator and saves them to CSV.

### prepare_initial_table: 
This function takes a dictionary of workloads grouped by class and a filename as input. It writes the workloads to a CSV file. For each workload, it extracts the metrics (CPU, Memory, Network, Storage) and writes them to the file.

### normalize_data:
This function takes a filename as input. It reads the data from the file and normalizes the CPU, Memory, Network, and Storage data using the MinMaxScaler. The data is then denormalized to the scale of the worker node's maximum capacity. The normalized data is written to a new CSV file.

### aggregate_data:
This function takes a filename and an optional aggregate_minute parameter as input. It reads the data from the file and groups the workloads based on their ids. For each group, it aggregates the data every 5 minutes (or the specified aggregate_minute) and calculates the minimum, maximum, median, and mean values for the CPU, Memory, Network, and Storage data. It also creates two new columns for the beginning and end of the time period. The aggregated data is then written to a new CSV file.

### add_missing_metrics()
This function adds missing metrics to the data. It reads the data from a CSV file, renames some columns, and adds new columns for the missing metrics. If the metric is not available, it is set to NaN. The final data is written to a new CSV file.

### add_allocation_and_demand()
TODO

### add_workernode_metrics()
The function starts by reading the CSV file and grouping the workloads based on their IDs. It then iterates over a time range, checking which workloads begin at each time point. 

For each workload that begins at the current time, the function checks if it has already been processed. If not, it resets the available capacity of the worker node and checks if the maximum values of the workload are less than the available capacity of the worker node. If they are, the workload is added to the worker node and the available capacity is updated. 

The function then checks if there is any capacity left in the worker node. If there is, it assigns the next workload to the same worker node, as long as it fits. 

Finally, the function writes the updated data back to a new CSV file.

### assign_workernodes()
This function assigns workloads to worker nodes based on their maximum capacities. It reads the data from a CSV file, groups the data by workload id, and assigns each workload to a worker node if the maximum values of the workload are less than the available capacity of the worker node. The function also tries to pack multiple workloads into the same worker node if there is remaining capacity. The final data, including the assigned worker node id for each workload, is written to a new CSV file.

### generate_data()
This function generates the data. It loads a YAML configuration file, processes the configuration, creates workloads, saves the workloads to a CSV file, normalizes the data, aggregates the data, assigns workloads to worker nodes, and adds missing metrics. The aggregate_minute parameter specifies the time period for aggregating the data.

### API
The script also provides a Flask API with two endpoints:

@app.route('/display', methods=['GET'])
This endpoint generates the data and returns it as a CSV file in the response. The data is read from a CSV file and returned as a plain text response.

@app.route('/download', methods=['GET'])
This endpoint generates the data and allows it to be downloaded as a CSV file. The data is read from a CSV file and returned as a file download response.  

### Sample output
|WORKLOAD_ID|WL_CPU_USG_MIN|WL_CPU_USG_MAX|WL_CPU_USG_MED|WL_CPU_USG_AVG|WL_MEM_USG_MIN|WL_MEM_USG_MAX|WL_MEM_USG_MED|WL_MEM_USG_AVG|WL_NET_TRN_USG_MIN|WL_NET_TRN_USG_MAX|WL_NET_TRN_USG_MED|WL_NET_TRN_USG_AVG|WL_STR_WRT_USG_MIN|WL_STR_WRT_USG_MAX|WL_STR_WRT_USG_MED|WL_STR_WRT_USG_AVG|WL_GPU_USG_MIN|WL_GPU_USG_MAX|WL_GPU_USG_MED|WL_GPU_USG_AVG|ENERGY_CONSUMPTION_MIN|ENERGY_CONSUMPTION_MAX|ENERGY_CONSUMPTION_MEDIAN|ENERGY_CONSUMPTION_MEAN|WL_POD_ID|COLLECTION_TYPE|WN_CPU_MAX_CAPACITY|WN_MEM_MAX_CAPACITY|WN_GPU_MAX_CAPACITY|WN_STR_MAX_CAPACITY|WN_NET_MAX_CAPACITY|START_TIME|END_TIME|WL_CPU_ALC|WL_GPU_ALC|WL_NET_ALC|WL_STR_ALC|WL_MEM_ALC|WL_ENERGY_ALC|WL_CPU_DEM|WL_MEM_DEM|WL_GPU_DEM|WL_STR_DEM|WL_NET_DEM|WL_ENERGY_DEM|WN_CPU_AVAILABLE|WN_MEM_AVAILABLE|WN_GPU_AVAILABLE|WN_STR_AVAILABLE|WN_NET_AVAILABLE|WORKERNODE_ID|WN_SRART_TIME|WN_END_TIME|WL_NET_REC_USG_AVG|WL_NET_REC_USG_MED|WL_NET_REC_USG_MAX|WL_NET_REC_USG_MIN|WL_STR_RED_USG_AVG|WL_STR_RED_USG_MAX|WL_STR_RED_USG_MIN|WL_STR_RED_USG_MED|
|--|--|--|--|--|--|--|--|--|--|--|--|--|--|--|--|--|--|--|--|--|--|--|--|--|--|--|--|--|--|--|--|--|--|--|--|--|--|--|--|--|--|--|--|--|--|--|--|--|--|--|--|--|--|--|--|--|--|--|--|--|--|
|2|25.96060877204473|386.0800352131137|204.4888685756365|205.3889737401456|0.0062436275537025|0.0229746883136906|0.0148285225427992|0.0148918817167551|0.0002755532277147|0.0058524118314796|0.0030304361280759|0.003055864231221|0.004807034722829|0.0218267424002211|0.0135622592173015|0.0136421968715723|0.0|0.0|0.0|0.0|4.046923473258565|4.1516903051667775|4.098838117241531|4.099228296520657|2|BatchProcessing|102400|12.1|128|16|8|2024-02-08 16:40:00|2024-02-08 16:45:00|9589.61995474302|0.0|0.1499907541979785|0.4533321553913135|0.4583226097676234|7.562462196711141|9110.138957005867|0.4354064792792422|0.0|0.4306655476217478|0.1424912164880795|7.184339086875584|92160.0|10.89|115.2|14.4|7.2|1|