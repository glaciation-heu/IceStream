import ast
import abc
import time
import json
import logging
import numpy as np
import matplotlib.pyplot as plt

from pathlib import Path
from datetime import datetime
from sklearn.metrics import mean_squared_error, mean_absolute_percentage_error


class Forecaster(metaclass=abc.ABCMeta):

    def __init__(self, 
        name: str,
        history: np.array,
        n_periods=1,
        evaluate=0.0,
    ):
        """
        :param name: model name
        :param history: historical data to be used for training
        :param n_periods: how many upcoming periods to be predicted
        :param evaluate: percentage to be used for evaluation to produce MSE, MAE
        """
        self.name = name
        self.history = history
        self.n_periods = n_periods
        self.evaluate = evaluate
        self.get_dump_path()

    
    @abc.abstractmethod
    def fit(self,):
        """ Fit the model with history """
        raise NotImplementedError 
    

    @abc.abstractmethod
    def predict(self,):
        """ Predict and return n_periods prediction, lower and upper bounds """
        raise NotImplementedError 
    

    @abc.abstractmethod
    def eval_fit(self,):
        """ 
        Rolling eval and update based on evaluation size/portion.
        """
        raise NotImplementedError
    

    @abc.abstractmethod
    def run(self,):
        """ Run with input data and dump JSON results """
        raise NotImplementedError


    def dump(self, exclude_list=None):
        """ Dump JSON results 
        
        :parameter exclude_list: a list of keys to be excluded for each model before dumping
        """
        for p in list(filter(lambda a: not a.startswith('__'), self.__dict__.keys())):
            if type(self.__dict__[p]) is np.ndarray:
                self.__dict__[p] = self.__dict__[p].tolist()
        results = self.__dict__
        print(f'results: {results}')
        if exclude_list:
            for k in exclude_list:
                results.pop(k)
        results['model'] = str(results['model'])
        results['dump_path'] = results['dump_path'].as_posix()

        # Serializing json
        logging.debug(f'results to dump: {results}')
        json_object = json.dumps(ast.literal_eval(str(results)))

        # Writing to sample.json
        with open(Path(self.dump_path, f'{self.name}_output.json'), 'w') as outfile:
            outfile.write(json_object)

        # Save test plot

        if 'test_pred' in self.__dict__.keys():
            f, ax = plt.subplots() 
            x = np.arange(len(self.test))
            # Plot train
            #plt.plot(np.arange(len(self.history)-len(self.test)), self.history[:-len(self.test)])
            plt.scatter(x, self.test, marker='x')
            plt.plot(x, self.test_pred)
            # Confidence interval
            plt.fill_between(
                x,
                #x+len(self.history)-len(self.test), 
                self.test_lower_bounds, 
                self.test_upper_bounds,
                alpha=.1,
                color='b'
            )
            plt.title('Actual test samples vs. forecasts')
            plt.text(
                0.5, 
                0.9, 
                f'MAPE: {self.eval_results["mape"]}',
                ha='center', 
                va='top', 
                transform=ax.transAxes
            )
            plt.tight_layout()
            plt.savefig(Path(self.dump_path, f'{self.name}_eval_plot.pdf'))

        
    def get_dump_path(self,):
        """ Set and make a path to store results """
        cur_time = datetime.now()
        time_str = cur_time.strftime('%Y%m%d-%H%M%S%f')
        self.dump_path = Path.cwd() / time_str
        self.dump_path.mkdir()
