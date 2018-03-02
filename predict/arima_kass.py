#!/usr/bin/env python3
"""
https://www.analyticsvidhya.com/blog/2016/02/time-series-forecasting-codes-python/
"""
import pandas as pd
import numpy as np
import matplotlib.pylab as plt
from matplotlib.pylab import rcParams
rcParams['figure.figsize'] = 15, 6 # donno

from statsmodels.tsa.stattools import adfuller # to test stationary
from statsmodels.tsa.seasonal import seasonal_decompose
from statsmodels.tsa.stattools import acf, pacf
from statsmodels.tsa.arima_model import ARIMA

def test_stationarity(timeseries):
    #Determing rolling statistics
    rolmean = pd.rolling_mean(timeseries, window=12)
    rolstd = pd.rolling_std(timeseries, window=12)

    #Plot rolling statistics:
    orig = plt.plot(timeseries, color='blue',label='Original')
    mean = plt.plot(rolmean, color='red', label='Rolling Mean')
    std = plt.plot(rolstd, color='black', label = 'Rolling Std')
    plt.legend(loc='best')
    plt.title('Rolling Mean & Standard Deviation')
    plt.show()

    #Perform Dickey-Fuller test:
    print('Results of Dickey-Fuller Test:')
    dftest = adfuller(timeseries, autolag='AIC')
    dfoutput = pd.Series(dftest[0:4], index=['Test Statistic','p-value','#Lags Used','Number of Observations Used'])
    for key,value in dftest[4].items():
        dfoutput['Critical Value (%s)'%key] = value
    print(dfoutput)

def make_stationary_simples_methods(ts):
    ts_log = np.log(ts) # remove trends by penalizing higher values. can use log, square root, cube root.
    plt.plot(ts_log)
    plt.show()
    moving_avg = pd.rolling_mean(ts_log,12) # räkna ut rolling mean
    plt.plot(ts_log)
    plt.plot(moving_avg, color='red')
    plt.show()
    ts_log_moving_avg_diff = ts_log - moving_avg # subtracta roling mean för gör stationary?
    ts_log_moving_avg_diff.dropna(inplace=True) # remove NaNvalues
    print(ts_log_moving_avg_diff.head(12))
    test_stationarity(ts_log_moving_avg_diff)

def make_stationary_differencing(ts):
    ts_log = np.log(ts) # remove trends by penalizing higher values. can use log, square root, cube root.
    ts_log_diff = ts_log - ts_log.shift()
    ts_log_diff.dropna(inplace=True)
    test_stationarity(ts_log_diff) # 90% confidence. We can also take second or third order differences which might get even better results in certain applications

def make_stationary_decomposing(ts): # finns advance decomposition
    ts_log = np.log(ts) # remove trends by penalizing higher values. can use log, square root, cube root.
    decomposition = seasonal_decompose(ts_log)

    trend = decomposition.trend
    seasonal = decomposition.seasonal
    residual = decomposition.resid # residual är det intressanta, nya datan
    plt.subplot(411)
    plt.plot(ts_log, label='Original')
    plt.legend(loc='best')
    plt.subplot(412)
    plt.plot(trend, label='Trend')
    plt.legend(loc='best')
    plt.subplot(413)
    plt.plot(seasonal,label='Seasonality')
    plt.legend(loc='best')
    plt.subplot(414)
    plt.plot(residual, label='Residuals')
    plt.legend(loc='best')
    plt.tight_layout()
    plt.show()

    ts_log_decompose = residual
    ts_log_decompose.dropna(inplace=True)
    test_stationarity(ts_log_decompose)
    return ts_log_decompose

def calc_p_q(ts):
    ts_log = np.log(ts) # remove trends by penalizing higher values. can use log, square root, cube root.
    ts_log_diff = ts_log - ts_log.shift()
    ts_log_diff.dropna(inplace=True)


    lag_acf = acf(ts_log_diff, nlags=20) # calc q
    lag_pacf = pacf(ts_log_diff, nlags=20, method='ols') # calc p

    #Plot ACF:
    plt.subplot(121)
    plt.plot(lag_acf)
    plt.axhline(y=0,linestyle='--',color='gray')
    plt.axhline(y=-1.96/np.sqrt(len(ts_log_diff)),linestyle='--',color='gray')
    plt.axhline(y=1.96/np.sqrt(len(ts_log_diff)),linestyle='--',color='gray')
    plt.title('Autocorrelation Function')

    #Plot PACF:
    plt.subplot(122)
    plt.plot(lag_pacf)
    plt.axhline(y=0,linestyle='--',color='gray')
    plt.axhline(y=-1.96/np.sqrt(len(ts_log_diff)),linestyle='--',color='gray')
    plt.axhline(y=1.96/np.sqrt(len(ts_log_diff)),linestyle='--',color='gray')
    plt.title('Partial Autocorrelation Function')
    plt.tight_layout()

    plt.show()

def arima(ts):
    ts_log = np.log(ts) # remove trends by penalizing higher values. can use log, square root, cube root.
    ts_log_diff = ts_log - ts_log.shift()
    ts_log_diff.dropna(inplace=True)
    # AR model
    # model = ARIMA(ts_log, order=(2, 1, 0))
    # results_AR = model.fit(disp=-1)
    # plt.plot(ts_log_diff)
    # plt.plot(results_AR.fittedvalues, color='red')
    # plt.title('RSS: %.4f'% sum((results_AR.fittedvalues-ts_log_diff)**2))

    # MA model
    # model = ARIMA(ts_log, order=(0, 1, 2))
    # results_MA = model.fit(disp=-1)
    # plt.plot(ts_log_diff)
    # plt.plot(results_MA.fittedvalues, color='red')
    # plt.title('RSS: %.4f'% sum((results_MA.fittedvalues-ts_log_diff)**2))

    # Combined model
    model = ARIMA(ts_log, order=(2, 1, 2)) # 2, 1, 2 | denna stämde best överens med orginal (log_diff) och därför används den. Behöver testa detta själv för att se vilken som stämmer bäst.
    results_ARIMA = model.fit(disp=-1)
    plt.plot(ts_log_diff)
    plt.plot(results_ARIMA.fittedvalues, color='red')
    plt.title('RSS: %.4f'% sum((results_ARIMA.fittedvalues-ts_log_diff)**2))

    # plt.show()
    return results_ARIMA

def scale_to_original(results_ARIMA, ts):
    predictions_ARIMA_diff = pd.Series(results_ARIMA.fittedvalues, copy=True) # skalar om till orginallvärden för att se hur bra det stämmer.
    print(predictions_ARIMA_diff.head())

    predictions_ARIMA_diff_cumsum = predictions_ARIMA_diff.cumsum() # väga upp för lag 1 som gör att någon inte kansubtrahera med något.
    print(predictions_ARIMA_diff_cumsum.head())

    ts_log = np.log(ts)
    predictions_ARIMA_log = pd.Series(ts_log.ix[0], index=ts_log.index)
    predictions_ARIMA_log = predictions_ARIMA_log.add(predictions_ARIMA_diff_cumsum,fill_value=0)
    print(predictions_ARIMA_log.head())

    # visa forecasten - stämmer inte, är kass.
    predictions_ARIMA = np.exp(predictions_ARIMA_log)
    plt.plot(ts)
    plt.plot(predictions_ARIMA)
    plt.title('RMSE: %.4f'% np.sqrt(sum((predictions_ARIMA-ts)**2)/len(ts)))
    plt.show()

dateparse = lambda dates: pd.datetime.strptime(dates, "%Y-%m") # lambda function to parse the dates from file
data = pd.read_csv('AirPassengers.csv', parse_dates=True, index_col='Month',date_parser=dateparse) # read data from file and parse the strins with dates to datetime objects
ts = data["#Passengers"] # make to a timeseries
print(data["#Passengers"])
# plt.plot(ts) # plot timeseries
# plt.show()
# test_stationarity(ts)
# make_stationary_differencing(ts)
# transofrmation för make stationary
# ts = make_stationary_decomposing(ts) om kör denna krashar combined model för finns NaN värden
# calc_p_q(ts)
# arima_data = arima(ts)
# scale_to_original(arima_data, ts)
