import time
import logging
import numpy as np
import pmdarima as pm

from util import data_utils
from model.forecaster import Forecaster
from sklearn.metrics import mean_squared_error, mean_absolute_percentage_error
from pmdarima import model_selection
from pmdarima.arima import auto_arima


class AutoARIMA(Forecaster):

    def __init__(self, 
        history: np.array,
        n_periods=1,
        evaluate=0.0,
        **kw_args
    ):
        """
        Initialize the Auto ARIMA forecaster
    
        :param name: model name
        :param history: historical data to be used for training
        :param n_periods: how many upcoming periods to be predicted
        :param evaluate: percentage to be used for evaluation to produce MSE, MAE
        :param **kw_args: dictionary for args of auto_arima such as m (default=1 meaning no seasonality)
        """
        super().__init__('AutoARIMA', history, n_periods, evaluate, **kw_args)

        try:
            logging.basicConfig(
                filename=f"{self.dump_path}/run.log",
                filemode="w",
                format="%(name)s - %(levelname)s - %(message)s",
                level=logging.DEBUG,
            )
            self.model = auto_arima(
                self.history,
                trace=True,
                D=1,
                error_action='ignore',
                suppress_warnings=True,
                **kw_args
            )
            self.run()
        except Exception as e:
            logging.exception('Cannot run AutoARIMA, simply set the prediction to previous value')
            self.prediction = self.history[-1]
            self.dump()
    
    
    def fit(self,):
        """ Fit the model with history """
        self.model.fit(self.history)
    
    
    def predict(self,):
        """ Predict and return n_periods prediction, lower and upper bounds """
        preds, conf_int =  self.model.predict(
            n_periods=self.n_periods,
            return_conf_int=True
        )
        logging.debug(f'test predictions: {preds}')
        logging.debug(f'test confidence intervals: {conf_int}')

        return preds, conf_int[:,0], conf_int[:,1]
    
    
    def eval_fit(self,):
        """ 
        Rolling eval and update based on evaluation size/portion.
        """
        train, test = model_selection.train_test_split(
            self.history,
            test_size=self.evaluate
        ) 
        # Rolloing evaluation
        predictions = []
        upper_bounds = []
        lower_bounds = []
        self.model.fit(train)
        for i in range(np.array(test).shape[0]):
            pred, conf_int = self.model.predict(
                n_periods=1, 
                return_conf_int=True
            )
            predictions.append(pred[0])
            upper_bounds.append(conf_int[0][1])
            lower_bounds.append(conf_int[0][0])
            # Update
            self.model.update(test[i])

        self.test_upper_bounds = upper_bounds
        self.test_lower_bounds = lower_bounds

        self.test_pred = np.array(predictions)
        self.test = np.array(test)
        self.eval_results = {
            'mape': np.round(
                mean_absolute_percentage_error(self.test, self.test_pred), 
                2
            ),
            'mse': np.round(
                mean_squared_error(self.test, self.test_pred),
                2
            )
        }

    
    def run(self,):
        """ Run with input data and dump JSON results """
        
        start_time = time.time()
        if self.evaluate > 0:
            logging.info('Rolling evaluate with {self.eval} as test, then fit')
            self.eval_fit()
        else:
            logging.info('Fitting the model')
            self.fit()

        # Predict for the next period
        logging.info('Predicting the next period')
        pred, conf_int = self.model.predict(
            n_periods=1, 
            return_conf_int=True
        )
        self.prediction = pred[0]
        self.upper_bound = conf_int[0][1]
        self.lower_bound = conf_int[0][0]

        self.fit_predict_time = round(time.time() - start_time, 2)
        logging.info(f'Used {self.fit_predict_time} seconds to fit')

        self.dump()
        logging.info(f'Dumping the results into {self.dump_path}')



if __name__ == "__main__":
   
    # From KG
    query = """
    prefix om: <http://www.ontology-of-units-of-measure.org/resource/om-2/>
    prefix prov: <http://www.w3.org/ns/prov#> 
    prefix xsd: <http://www.w3.org/2001/XMLSchema#> 

    SELECT ?measure
    WHERE {
      ?subject rdf:type om:Measure .
      ?subject om:hasNumericalValue ?measure .
      ?subject prov:generatedAtTime ?date .
    }
    ORDER BY ASC(?date)
    """
    #ts_from_kg = data_utils.get_timeseries(query) 

    datasets = [
        np.arange(1,30,2),
#        np.random.randint(5, size=11),
#        pm.datasets.load_wineind(),
#        ts_from_kg
    ]
    for dataset in datasets:
        print(f'dataset: {dataset}')
        forecaster = AutoARIMA(
            dataset, 
            evaluate=10,
         #   m=12
        )

