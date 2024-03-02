import numpy as np
import forecast

from flask import Flask, request


app = Flask(__name__)


@app.route('/')
def welcome():
    return 'This is Forecasting API from Glaciation'


@app.route('/forecast', methods=['POST'])
def pred():
    content_type = request.headers.get('Content-Type')
    if (content_type == 'application/json'):
        json = request.json
        if 'history' in json:
            dataset = json['history']
            m = json.get('m', 1)
            forecaster = forecast.Forecaster(
                dataset,
                evaluate=0.0,
                m=m
            )

            results = {
                'history': dataset,
                'prediction': np.round(forecaster.prediction,5),
                'upper_bound': np.round(forecaster.upper_bound,5),
                'lower_bound': np.round(forecaster.lower_bound,5)
            }
            return results
        else:
            return 'Please provide valid history for forecasting', 400
    else:
        return 'Content-Type is not supported!'
    

if __name__ == '__main__':
    app.run('localhost', 5000, debug=True)
    #app.run('0.0.0.0',5000,debug = False)
