import time
import talos
import logging
import numpy as np
import pmdarima as pm
import tensorflow as tf
import tensorflow_probability as tfp

from util import data_utils
from model.forecaster import Forecaster
from util.custom_keras import CustomSaveCheckpoint
from tensorflow import keras
from sklearn.metrics import mean_squared_error, mean_absolute_percentage_error
from pmdarima import model_selection
from pmdarima.arima import auto_arima
from tensorflow.keras.models import Sequential
from tensorflow.keras.callbacks import EarlyStopping
from tensorflow.keras.layers import Dense, LSTM, Conv1D, Flatten, Activation, Dropout, BatchNormalization, Input
from tensorflow.keras.optimizers import Adam, RMSprop
from sklearn.preprocessing import MinMaxScaler


class VarLayer(tfp.layers.DenseVariational):
    def __init__(
        self,
        name,
        units,
        make_prior_fn,
        make_posterior_fn,
        kl_weight,
        activation,
        **kwargs
    ):
        super().__init__(
            units=units,
            make_prior_fn=make_prior_fn,
            make_posterior_fn=make_posterior_fn,
            name=name,
            kl_weight=kl_weight,
            activation=activation,
            **kwargs
        )

    def get_config(self):
        config = super(VarLayer, self).get_config()
        config.update({
            'name': self.name,
            'units': self.units,
            'activation': self.activation
        })

        return config

    def call(self, inputs):
        return super(VarLayer, self).call(inputs)


class HBNN(Forecaster):

    def __init__(self, 
        history: np.array,
        name='HBNN',
        window_size=168,
        n_periods=1,
        evaluate=10,
        **kw_args
    ):
        """
        Initialize the HBNN forecaster
    
        :param name: model name
        :param history: historical data to be used for training
        :param window_size: to be used for generating window dataset (X,y) format for training
        :param n_periods: how many upcoming periods to be predicted
        :param evaluate: percentage to be used for evaluation to produce MSE, MAE
        :param **kw_args: dictionary for args of model 
        """
        super().__init__(name, history, n_periods, evaluate)

        try:
            logging.basicConfig(
                filename=f"{self.dump_path}/run.log",
                filemode="w",
                format="%(name)s - %(levelname)s - %(message)s",
                level=logging.DEBUG,
            )

            # Create HBNN model
            self.window_size = window_size
            self.validation=0.2
            self.run()

        except Exception as e:
            logging.exception('Cannot run HBNN, simply set the prediction to previous value')
            self.prediction = self.history[-1]
            self.dump(exclude_list=['scaler', 'current'])
    
    
    def fit(self,):
        """ Fit the model with history """
        self.eval_fit()
    
    
    def predict(self,):
        """ Predict and return n_periods prediction, lower and upper bounds """
        preds, conf_int =  self.model.predict(
            n_periods=self.n_periods,
            return_conf_int=True
        )
        logging.debug(f'test predictions: {preds}')
        logging.debug(f'test confidence intervals: {conf_int}')

        return preds, conf_int[:,0], conf_int[:,1]
    
    
    def run(self,):
        """ Run with input data and dump JSON results """
        
        start_time = time.time()
        if self.evaluate > 0:
            logging.info('Evaluate with {self.eval} as test')
            self.eval_fit()
        else:
            logging.info('Fitting the model')
            self.fit()

        # Predict for the next period
        logging.info('Predicting the next period')
        last_window = self.scaler.transform(
            self.history[-self.window_size:].reshape(-1,1)  
        ).reshape(1,-1,1)
        print(f'last window: {last_window}')
        pred_dist = self.model(last_window)
        mean = pred_dist.mean().numpy()
        std = pred_dist.stddev().numpy()
        self.prediction = self.scaler.inverse_transform(mean)[0]
        self.upper_bound = self.scaler.inverse_transform(mean+3.*std)[0]
        self.lower_bound = self.scaler.inverse_transform(mean-3.*std)[0]

        self.fit_predict_time = round(time.time() - start_time, 2)
        logging.info(f'Used {self.fit_predict_time} seconds to fit')

        self.dump(exclude_list=['current', 'scaler'])
        logging.info(f'Dumping the results into {self.dump_path}')


    def neg_loglikelihood(self, targets, estimated_dist):
        return -estimated_dist.log_prob(targets)


    def save_model(self,):
        """ Save the current model under training """
        self.current.save_weights(
            str(self.dump_path) + '/' + self.name + '_weights.tf',
            save_format='tf'
        )    
    

    def eval_fit(self,):
        """ Training Talos model, eval with last few examples """
        
        # Scaler test
        self.scaler = MinMaxScaler((-1,1))
        transformed_history = self.scaler.fit_transform(self.history.reshape(-1,1))
        
        # Create window dataset from history
        windowed_history = data_utils.window_dataset(transformed_history, self.window_size)                        
        
        # Prepare training and validatoin data

        data, labels = windowed_history
        train_size = int(data.shape[0] * (1.0 - self.validation))
        logging.info(f'data size: {data.shape[0]}\ttrain size: {train_size}')
        x_train = data[:train_size]
        y_train = labels[:train_size]
        x_val = data[train_size:]
        y_val = labels[train_size:]

        # Talos experiments parameter list
        self.parameter_list = {
            'first_conv_dim': [16],
            'first_conv_kernel': [5],
            'first_conv_activation': ['relu'],
            'second_lstm_dim': [8],
            'first_dense_dim': [8],    
            'first_dense_activation': ['relu'],
            'dense_kernel_init': ['glorot_uniform'],
            'batch_size': [32, 64, 128],
            'epochs': [500],
            'patience': [10],
            'optimizer': ['adam'],
            'lr': [1e-2, 1e-3, 1e-4],
            #'momentum': [0.9, 0.99],
            #'decay': [1E-3, 1E-4, 1E-5],
        }

        # Model

        def _prior(kernel_size, bias_size, dtype=None):
            n = kernel_size + bias_size
            prior = Sequential([
                tfp.layers.DistributionLambda(
                    lambda t: tfp.distributions.MultivariateNormalDiag(
                        loc=tf.zeros(n),
                        scale_diag=tf.ones(n)
                    )
                )
            ])
            return prior
        

        def _posterior(kernel_size, bias_size, dtype=None):
            n = kernel_size + bias_size
            posterior = Sequential([
                tfp.layers.VariableLayer(
                    tfp.layers.MultivariateNormalTriL.params_size(n)
                ),
                tfp.layers.MultivariateNormalTriL(n)
            ])
            return posterior
            

        def _hbnn(x, y, x_val, y_val, params):
            self.current = Sequential([
                Conv1D(
                    filters=params['first_conv_dim'],
                    kernel_size=params['first_conv_kernel'],
                    strides=1,
                    padding='causal',
                    activation=params['first_conv_activation'],
                    input_shape=(self.window_size, 1)
                ),
                LSTM(params['second_lstm_dim']),
                #VarLayer(
                #    name='var',
                #    units=params['first_dense_dim'],
                #    make_prior_fn=_prior,
                #    make_posterior_fn=_posterior,
                #    kl_weight=1./x.shape[0],
                #    activation=params['first_dense_activation']
                #),
                Dense(2),
                tfp.layers.IndependentNormal(1)
            ])
            print(self.current.summary())
            
            if params['optimizer'] == 'adam':
                opt = Adam(learning_rate=params['lr'])
            elif params['optimizer'] == 'rmsprop':
                opt = RMSprop(learning_rate=params['lr'])

            self.current.compile(
                optimizer=opt,
                loss=self.neg_loglikelihood,
                metrics=['mae', 'mse', 'mape']
            )
            
            check_point = CustomSaveCheckpoint(self)
            es = EarlyStopping(
                monitor='val_loss',
                mode='min',
                verbose=1,
                patience=params['patience']
            )

            out = self.current.fit(
                data, 
                labels, 
                validation_data=(x_val, y_val),
                epochs=params['epochs'],
                batch_size=params['batch_size'],
                callbacks=[es, check_point],
            )

            return out, self.model

        # Set best val loss for checkpoint in the experiment
        self.best_val_loss = np.Inf

        scan_object = talos.Scan(
            x=x_train,
            y=y_train,
            x_val=x_val,
            y_val=y_val,
            params=self.parameter_list,
            model=_hbnn,
            experiment_name='hbnn'
        )

        logging.info(f'Best val loss: {self.best_val_loss}')

        pred_dist = self.model(x_val)
        pred_mean = pred_dist.mean().numpy()
        pred_ub = pred_mean + 3. * pred_dist.stddev().numpy()
        pred_lb = pred_mean - 3. * pred_dist.stddev().numpy()

        # Evaluation for plot
        predictions = self.scaler.inverse_transform(pred_mean).flatten().tolist()
        upper_bounds = self.scaler.inverse_transform(pred_ub).flatten().tolist()
        lower_bounds = self.scaler.inverse_transform(pred_lb).flatten().tolist()

        self.test_upper_bounds = upper_bounds[-self.evaluate:]
        self.test_lower_bounds = lower_bounds[-self.evaluate:]

        self.test_pred = np.array(predictions)[-self.evaluate:].flatten().tolist()
        self.test = self.history[-self.evaluate:].flatten().tolist()
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
        np.arange(1,1000,2),
#        np.random.randint(5, size=11),
#        pm.datasets.load_wineind(),
#        ts_from_kg
    ]
    for dataset in datasets:
        print(f'dataset: {dataset}')
        forecaster = HBNN(
            dataset, 
            evaluate=10,
        )

