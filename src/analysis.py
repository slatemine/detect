
#from scipy.fftpack import fft, fftfreq
from sklearn import linear_model
from sklearn_pandas import DataFrameMapper

import pandas as pd
import datetime, logging
import matplotlib.pyplot as plt
import statsmodels.api as sm

class Analysis:

    def __init__(self, geoip):
        self.geoip = geoip

    def plot_csv(self, results, job=None, type='alert' ):
        logger = logging.getLogger(__name__)
        logger.debug(results)
        name = job['name']
        logger.info('Processing results for: %s'%(name))

        df = pd.read_csv( job['data'] )
        df.plot(title=name)
        plt.show()
        logger.info(df)

    def detect(self, results, job=None, type='alert' ):
        logger = logging.getLogger(__name__)
        logger.debug(results)
        name = job['name']
        logger.info('Processing results for: %s'%(name))

        df = pd.read_csv( job['data'] )
        n = len(df)
        sdg = linear_model.SGDRegressor()

        mapper = DataFrameMapper( [
            ( 'value', None)
        ])
        df_train = df[:n/2]['value'].as_matrix()
        df_test = df[n/2:]['value'].as_matrix()

        logger.info([df_train])
#        ft_df = fft(df['value'].as_matrix())
#        ft_x = fftfreq(len(df['value']))

        df.plot(title=name)
#        r = sdg.fit(df_train['value'].as_matrix(),df_test['value'].as_matrix())
#        logger.info(r)
        self.decompose(df['value'])
        plt.show()
        logger.info(df)


    # Naive decomposition
    def decompose(self, data):
        logger = logging.getLogger(__name__)
        data.interpolate(inplace=True)
        logger.info(data.head(16))
        res = sm.tsa.seasonal_decompose(data, model='additive')
        plt = res.plot()
        plt.show()