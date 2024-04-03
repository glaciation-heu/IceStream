import json
import influxdb_client

from influxdb_client.domain.write_precision import WritePrecision
from datetime import datetime, timezone, time, timedelta
from influxdb_client.client.write_api import SYNCHRONOUS


DATA_ACCESS_BUCKET = 'data_access'
ENERGY_CONSUMPTION_BUCKET = 'energy_consumption'
ORG = 'glaciation'
TOKEN = 'Rs03_DH_rzXgNAx5s0fHLfAKsnbSB1W3wBBOvBseICw13ibL8q0bVxUUJ7Ynu4D20J-9TGSoXHDwWaRFtUrZrg=='
#URL = 'http://localhost:8086'
# Minikube setting
ORG = 'primary'
TOKEN = 'YiORLlU2bDNwPjnOiFS4dAJDH61JHLFCUV6VkVvUiN_O92BS3KB63y1Uxj6eSX0Zc3yzn0Mzn3GyeJeLO_BWuw=='
URL = 'http://10.244.0.21:8086'


client = influxdb_client.InfluxDBClient(
    url = URL,
    token = TOKEN,
    org = ORG
)


def writeDataAccessRecord(data_access_record):
    """
    Write data access record to InfluxDB

    Parameters:
        data_access_record: data access record object
    """
    write_api = client.write_api(write_opetions=SYNCHRONOUS)
    # Write data access record to InfluxDB 
    r = influxdb_client.Point('data_access') \
            .tag('requestId', data_access_record.request_id) \
            .tag('dataId', data_access_record.data_id) \
            .field('value', 1) \
            .time(data_access_record.time, write_precision=WritePrecision.MS)
    write_api.write(bucket=DATA_ACCESS_BUCKET, org=ORG, record=r)
    

def readDataAccessRecord(dataId, start_time=None, end_time=None):
    """
    Read data access record for a given dataId
    
    Parameters:
        dataId: the dataId of a data access record
        start_time: for filtering, optional
        end_time: for filtering, optional

    Returns:
        A list of JSON strings
    """
    query_api = client.query_api()
    if start_time is None:
        start_time = '2000-01-01T00:00:00Z'
    if end_time is None:
        end_time = datetime.now(timezone.utc)
        end_time = end_time.strftime('%Y-%m-%dT%H:%M:%SZ')

    query = f'from(bucket:"{DATA_ACCESS_BUCKET}")\
                |> range(start: {start_time}, stop: {end_time})\
                |> filter(fn:(r) => r._measurement == "data_access")\
                |> filter(fn:(r) => r.dataId == "{dataId}")'
    result = query_api.query(org=ORG, query=query)

    results = []
    for table in result:
        for record in table.records:
            results.append(
                json.dumps({
                    'time': record.get_time().strftime('%Y-%m-%dT%H:%M:%S.%fZ'), 
                    'dataId': record.values.get('dataId'),
                    'requestId': record.values.get('requestId'),
                })
            )

    return results


def writePredictionResults(metric):
    """
    Write prediction results - metric - into InfluxDB

    Parameters:
        metric: Metric object containing predition results
    """
    write_api = client.write_api(write_opetions=SYNCHRONOUS)
    
    print(metric)

    ## Write time series to InfluxDB

    timeseries = []
    for i, v in enumerate(metric.timeseries):
        r = influxdb_client.Point('timeseries') \
                .tag('metricId', metric.metric_id) \
                .tag('aggregation_interval', metric.aggregation_interval) \
                .field('value', v) \
                .time(datetime.combine(metric.time[i], time(0,0,0)))
        timeseries.append(r)
    write_api.write(bucket=ENERGY_CONSUMPTION_BUCKET, org=ORG, record=timeseries)

    ## Write prediction record to InfluxDB 

    forecasting_time = [
        datetime.combine(
            max(metric.time)+timedelta(seconds=metric.aggregation_interval)*(i+1), time(0,0,0)) 
            for i in range(metric.forecasting_period)
    ]
    print(f'forecasting time: {forecasting_time}') 
    forecasting_timeseries = []
    for i,v in enumerate(forecasting_time):
        r = influxdb_client.Point('forecasting') \
                .tag('metricId', metric.metric_id) \
                .tag('aggregation_interval', metric.aggregation_interval) \
                .tag('forecasting_model', metric.forecasting_model) \
                .tag('forecasting_time', v) \
                .tag('input_size', len(metric.timeseries)) \
                .field('forecasting_value', metric.forecasting_values[i]) \
                .field('forecasting_upper', metric.forecasting_upper_bounds[i]) \
                .field('forecasting_lower', metric.forecasting_lower_bounds[i]) \
                .time(datetime.combine(max(metric.time), time(0,0,0)))
        print(f'Writing to InfluxDB cloud: {r.to_line_protocol()} ...')
        forecasting_timeseries.append(r)
    write_api.write(bucket=ENERGY_CONSUMPTION_BUCKET, org=ORG, record=forecasting_timeseries)


def readPredictionResults(metricId, forecasting_time):
    """
    Read prediction results for the given metricId

    Parameters:
        metricId: metricId to retrieve prediction results
        forecasting_time: the time of forecasting happend

    Returns:
        A list of JSON strings 
    """
    query_api = client.query_api()
    start_time = '2000-01-01T00:00:00Z'
    end_time = datetime.now(timezone.utc)
    end_time = end_time.strftime('%Y-%m-%dT%H:%M:%SZ')
    
    query = f'from(bucket:"{ENERGY_CONSUMPTION_BUCKET}")\
                |> range(start: {start_time}, stop: {end_time}) \
                |> filter(fn:(r) => r._measurement == "forecasting")\
                |> filter(fn:(r) => r.metricId == "{metricId}") \
                |> filter(fn:(r) => r._time == {forecasting_time}) \
                |> group(columns: ["metricId","_time"]) \
                |> sort(columns: ["forecasting_time"])'
    result = query_api.query(org=ORG, query=query)

    to_return = {
        'forecasting_values': [],
        'forecasting_upper_bounds': [],
        'forecasting_lower_bounds': [],
        'time': [],
        'timeseries': []
    }

    ## Get the JSON format of prediction including timeseries input

    for table in result:
        for i, record in enumerate(table.records):
            #print(record.values)
            # Only do once
            if i == 0:
                to_return['aggregation_interval'] = record.values.get('aggregation_interval')
                to_return['forecasting_model'] = record.values.get('forecasting_model')
                to_return['metricId'] = record.values.get('metricId')
                to_return['forecasting_time'] = record.get_time()
                to_return['input_size'] = record.values.get('input_size')
            if record.get_field() == 'forecasting_lower':
                to_return['forecasting_lower_bounds'].append(record.get_value()) 
            elif record.get_field() == 'forecasting_upper':
                to_return['forecasting_upper_bounds'].append(record.get_value())
            elif record.get_field() == 'forecasting_value':
                to_return['forecasting_values'].append(record.get_value())
    to_return['forecasting_period'] = len(to_return['forecasting_values'])

    ## Get time series used as an input for this prediction

    for i in range(int(to_return['input_size'])):
        to_return['time'].append(
            (to_return['forecasting_time'] - i*timedelta(
                    seconds=int(to_return['aggregation_interval'])
            )).strftime('%Y-%m-%dT%H:%M:%SZ')
        )
    to_return['time'].reverse()

    # Stop is exclusive in filtering Flux below
    stop = (datetime.strptime(to_return['time'][-1], '%Y-%m-%dT%H:%M:%SZ') \
                + timedelta(seconds=int(to_return['aggregation_interval']))) \
                .strftime('%Y-%m-%dT%H:%M:%SZ')

    # Get timeseries
    query = f'from(bucket:"{ENERGY_CONSUMPTION_BUCKET}") \
                |> range(start: {to_return["time"][0]}, stop: {stop}) \
                |> filter(fn:(r) => r._measurement == "time_series")\
                |> filter(fn:(r) => r.metricId == "{metricId}") \
                |> sort(columns: ["_value"])'
    result = query_api.query(org=ORG, query=query)
    for table in result:
        for i, record in enumerate(table.records):
            to_return['timeseries'].append(record.get_value())

    ## Remove unneccessary keys and create JSON string

    to_return.pop('forecasting_time')
    to_return.pop('input_size')
    to_return = json.dumps(to_return)
    #print(to_return)
    
    return to_return


def readTimeseries(metricId, start_time=None, end_time=None):
    """ Return timeseries for the metricId
    
    Parameters:
        metridId: the metridId for the timeseries
        start_time: to filter the timeseries, optional
        end_time: to filter the timeseries, optional

    Returns:
        A list of JSON strings
    
    """
    query_api = client.query_api()
    if start_time is None:
        start_time = '2000-01-01T00:00:00Z'
    if end_time is None:
        end_time = datetime.now(timezone.utc)
        end_time = end_time.strftime('%Y-%m-%dT%H:%M:%SZ')

    query = f'from(bucket:"{ENERGY_CONSUMPTION_BUCKET}")\
                |> range(start: {start_time}, stop: {end_time})\
                |> filter(fn:(r) => r._measurement == "timeseries")\
                |> filter(fn:(r) => r.metricId == "{metricId}") \
                |> group(columns: ["{metricId}"]) \
                |> sort(columns: ["_time"])'
    result = query_api.query(org=ORG, query=query)

    to_return = {
        'time': [],
        'timeseries': []
    }
    for table in result:
        for i, record in enumerate(table.records):
            if i == 0:
                to_return['aggregation_interval'] = int(record.values.get('aggregation_interval'))
                to_return['metricId'] = metricId
            to_return['time'].append(record.get_time().strftime('%Y-%m-%dT%H:%M:%SZ'))
            to_return['timeseries'].append(record.get_value())

    print(to_return)
    return json.dumps(to_return)

if __name__ == '__main__':
    readPredictionResults('M1','2024-02-19T00:00:00Z')
