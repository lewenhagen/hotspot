#!/usr/bin/env python3
"""
https://www.digitalocean.com/community/tutorials/a-guide-to-time-series-forecasting-with-arima-in-python-3
"""
import warnings
import itertools
import pandas as pd
import numpy as np
import statsmodels.api as sm
from statsmodels.tsa.stattools import adfuller # to test stationary
from statsmodels.tsa.seasonal import seasonal_decompose
import matplotlib.pyplot as plt
import datetime
from dateutil import relativedelta
from sapphire import Sapphire
plt.style.use('fivethirtyeight')

def test_stationarity(timeseries):
    warnings.simplefilter("ignore")
    warnings.filterwarnings("ignore") # specify to ignore warning messages
    warnings.warn("deprecated", DeprecationWarning)
    #Determing rolling statistics
    rolmean = pd.rolling_mean(timeseries, window=84)
    rolstd = pd.rolling_std(timeseries, window=84)

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

def parameter_selection_for_arima(y):
    # Define the p, d and q parameters to take any value between 0 and 2
    p = d = q = range(0, 3)
    # Generate all different combinations of p, q and q triplets
    pdq = list(itertools.product(p, d, q))

    # Generate all different combinations of seasonal p, q and q triplets
    seasonal_pdq = [(x[0], x[1], x[2], (2016)) for x in list(itertools.product(p, d, q))]

    # print('Examples of parameter combinations for Seasonal ARIMA...')
    # print('SARIMAX: {} x {}'.format(pdq[1], seasonal_pdq[1]))
    # print('SARIMAX: {} x {}'.format(pdq[1], seasonal_pdq[2]))
    # print('SARIMAX: {} x {}'.format(pdq[2], seasonal_pdq[3]))
    # print('SARIMAX: {} x {}'.format(pdq[2], seasonal_pdq[4]))

    warnings.filterwarnings("ignore") # specify to ignore warning messages
    AIC_list = pd.DataFrame({}, columns=['param','param_seasonal','AIC'])
    for param in pdq:
        for param_seasonal in seasonal_pdq:
            try:
                mod = sm.tsa.statespace.SARIMAX(y,
                                                order=param,
                                                seasonal_order=param_seasonal,
                                                enforce_stationarity=False,
                                                enforce_invertibility=False)

                results = mod.fit()

                print('ARIMA{}x{} - AIC:{}'.format(param, param_seasonal, results.aic))
                temp = pd.DataFrame([[ param ,  param_seasonal , results.aic ]], columns=['param','param_seasonal','AIC'])
                AIC_list = AIC_list.append( temp, ignore_index=True)  # DataFrame append 는 일반 list append 와 다르게 이렇게 지정해주어야한다.
                del temp

            except:
                continue


    m = np.amin(AIC_list['AIC'].values) # Find minimum value in AIC
    l = AIC_list['AIC'].tolist().index(m) # Find index number for lowest AIC
    Min_AIC_list = AIC_list.iloc[l,:]



    mod = sm.tsa.statespace.SARIMAX(y,
                                    order=Min_AIC_list['param'],
                                    seasonal_order=Min_AIC_list['param_seasonal'],
                                    enforce_stationarity=False,
                                    enforce_invertibility=False)
    results = mod.fit()

    print("### Min_AIC_list ### \n{}".format(Min_AIC_list))

    print(results.summary().tables[1])

    results.plot_diagnostics(figsize=(15, 12))
    plt.show()
def fit_time_series(y):
    warnings.filterwarnings("ignore") # specify to ignore warning messages
    mod = sm.tsa.statespace.SARIMAX(y,
                                    # order=(1, 0, 1),
                                    order=(2, 1, 3),
                                    # seasonal_order=(0, 0, 0, 2016),
                                    enforce_stationarity=False,
                                    enforce_invertibility=False)

    results = mod.fit()
    print(results.aic)
    print(results.summary().tables[1])
    # results.plot_diagnostics(figsize=(15, 12))
    # plt.show()
    return results
    #
def validate_forecast_non_dynamic(results, y):
    pred = results.get_prediction(start=pd.to_datetime('2014-12-01 00:00'), end=pd.to_datetime('2014-12-07 23:00'), dynamic=False)
    #print(pred.predicted_mean) # lista med värden
    #print(pred.summary_frame())
    #print(dir(pred.prediction_results.results))
    pred_ci = pred.conf_int()
    #print(y)
    ax = y['2014':].plot(label='observed')
    pred.predicted_mean.plot(ax=ax, label='One-step ahead Forecast', alpha=.7)

    ax.fill_between(pred_ci.index,
                    pred_ci.iloc[:, 0],
                    pred_ci.iloc[:, 1], color='k', alpha=.2)

    ax.set_xlabel('Date')
    ax.set_ylabel('Crimes')
    plt.legend()

    plt.show()

    #average_error

    y_forecasted = pred.predicted_mean
    y_truth = y['2014-12-01':]

    # Compute the mean square error
    mse = ((y_forecasted - y_truth) ** 2).mean()
    print('The Mean Squared Error of our forecasts is {}'.format(round(mse, 2))) # Nära 0 är bra. 0 = perfect matchning mellan verklighet och forutspådd.

    return pred.predicted_mean

def validate_forecast_dynamic(results, y):
    pred_dynamic = results.get_prediction(start=pd.to_datetime('2014-12-01 00:00:00'), dynamic=True, full_results=True)
    pred_dynamic_ci = pred_dynamic.conf_int()
    # print(y.values)
    # plt.plot(y)
    # plt.show()
    ax = y["2014":].plot(label='observed')
    pred_dynamic.predicted_mean.plot(label='Dynamic Forecast', ax=ax)

    ax.fill_between(pred_dynamic_ci.index,
                    pred_dynamic_ci.iloc[:, 0],
                    pred_dynamic_ci.iloc[:, 1], color='k', alpha=.25)

    ax.fill_betweenx(ax.get_ylim(), pd.to_datetime('2014-12-01 00:00:00'), y.index[-1],
                     alpha=.1, zorder=-1)

    ax.set_xlabel('Date')
    ax.set_ylabel('CO2 Levels')

    plt.legend()
    plt.show()

    # Extract the predicted and true values of our time series
    y_forecasted = pred_dynamic.predicted_mean
    y_truth = y['2014-12-01 00:00:00':]

    # Compute the mean square error
    mse = ((y_forecasted - y_truth) ** 2).mean()
    print('The Mean Squared Error of our forecasts is {}'.format(round(mse, 2)))
    return pred_dynamic.predicted_mean

def forecast_steps(results, y):
    # Get forecast 500 steps ahead in future
    y = add_new_time_period(y)
    print(type(y))
    print(y)
    #print(y['Total Minutes_Amazon'].head())
    print(y.index.freq)
    print(type(results))
    print(dir(results))

    # pred_uc = results.forecast(steps=168) Om vi har frequenzy, utan lagt till datum
    y['forecast'] = results.predict(start = pd.to_datetime('2015-01-01'), dynamic= False)
    y[['crimes', 'forecast']].ix[-24:].plot(figsize=(12, 8))
    # Get confidence intervals of forecasts
    pred_ci = pred_uc.conf_int()

    ax = y.plot(label='observed', figsize=(20, 15))
    pred_uc.predicted_mean.plot(ax=ax, label='Forecast')
    ax.fill_between(pred_ci.index,
                    pred_ci.iloc[:, 0],
                    pred_ci.iloc[:, 1], color='k', alpha=.25)
    ax.set_xlabel('Date')
    ax.set_ylabel('CO2 Levels')

    plt.legend()
    plt.show()


def add_new_time_period(y):
    # print(y)
    # start = datetime.datetime.strptime("2015-01-01 00:00:00", "%Y-%m-%d %H:%M:%S")
    # date_list = [start + relativedelta.relativedelta(hours=x) for x in range(0,168)]
    # future = pd.DataFrame(index=date_list, columns= ["crimes"])
    # print(future)
    # future = future["crimes"]
    # future = future.astype("float64")
    #y = pd.concat([y, future])
    start = datetime.datetime.strptime("2015-01-01 00:00:00", "%Y-%m-%d %H:%M:%S")
    date_list = pd.date_range('2015-01-01 00:00:00', freq='1H', periods=168)
    future = pd.DataFrame(index=date_list)
    data = pd.concat([y, future])
    # y = y.append(future)
    #y = y.fillna(0)
    print(data)
    return data

def resize_result(res, ts_log, ts):
    #predictions_ARIMA_diff = pd.Series(y.fittedvalues, copy=True)
    #predictions_ARIMA_diff_cumsum = res.cumsum()
    #predictions_ARIMA_log = pd.Series(ts_log.ix[0], index=ts_log.index)
    #predictions_ARIMA_log = predictions_ARIMA_log.add(predictions_ARIMA_diff_cumsum,fill_value=0)
    #predictions_ARIMA_log.head()
    #print(predictions_ARIMA_log)
    #print(res.head())
    predictions_ARIMA = np.exp(res)
    plt.plot(ts)
    #print(predictions_ARIMA)
    plt.plot(predictions_ARIMA)
    plt.title('RMSE: %.4f'% np.sqrt(sum((predictions_ARIMA-ts)**2)/len(ts)))


    #print(np.exp(res))

    plt.show()
    return predictions_ARIMA


# dateparse = lambda dates: pd.datetime.strptime(dates, "%Y-%m-%d ") # lambda function to parse the dates from file
# data = pd.read_csv('data.csv', parse_dates=True, index_col="day", delimiter=",") # read data from file and parse the strins with dates to datetime objects
data = pd.read_csv('datas.csv', parse_dates=[0], keep_date_col=True, index_col=0, delimiter=",", header=None, names=["day", "crimes"]) # read data from file and parse the strins with dates to datetime objects
# data.sort_values(by="day")
data = data.sort_index()
o = data["crimes"] # make to a timeseries
y = np.log(o) # make more stationary. got  better results in stationary and fit
# y = o
#decomposition = seasonal_decompose(y)
#y = decomposition.resid # behöver en frequenzy för denna
# plt.plot(y) # plot timeseries
# plt.show()

# data = sm.datasets.co2.load_pandas()
# y = data.data
# The 'MS' string groups the data in buckets by start of the month and makes average for each month
# y = y['crimes'].resample('MS').mean()
# The term bfill means that we use the value before filling in missing values
# y = y.fillna(np.nan)

# y = add_new_time_period(y)
#print(y)
# y.plot(figsize=(15, 6))
# plt.show()
# test_stationarity(y)
## parameter_selection_for_arima(y)
res = fit_time_series(y)
# plt.plot(y) # plot timeseries
# plt.show()
# pred = validate_forecast_non_dynamic(res, y) # working
pred = validate_forecast_dynamic(res, y) # kass
# #forecast_steps(res, y)
# values = resize_result(pred, y, o)
s = Sapphire([], pred)
v = np.array(pred)
v = v.reshape(7,24)
v = np.transpose(v)
# #print(v)
s.res_sum_mat = v
s.calc_gi()
