# Prediction Service
This microservice provides forecasting functionality based on historical timeseries data retrieved from DKG.
The service is developed in ```Python 3.9.18```.

## Implemented methods
- ARIMA
- HBNN

## Structure


```python
/data               # the folder contains sample KG snippet used for experiments
/model              # the folder contains implemented models 
/util               # the folder contains utils
forecast_api.py     # flask api, may not be needed at the end depending on system requirements
requirements.txt    # required packages and their versions
run.sh              # run test using mock data, useful to test added method
test.py             # test script
```



