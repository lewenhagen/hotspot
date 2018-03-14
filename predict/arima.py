#!/usr/bin/env python3
"""
https://www.digitalocean.com/community/tutorials/a-guide-to-time-series-forecasting-with-arima-in-python-3
"""
import warnings
import itertools
import pandas as pd
import numpy as np
import statsmodels.api as sm
import matplotlib.pyplot as plt
plt.style.use('fivethirtyeight')
warnings.filterwarnings("ignore") # specify to ignore warning messages

def parameter_selection_for_arima():
    # Define the p, d and q parameters to take any value between 0 and 2
    p = d = q = range(0, 5)
    # Generate all different combinations of p, q and q triplets
    pdq = list(itertools.product(p, d, q))

    # Generate all different combinations of seasonal p, q and q triplets
    seasonal_pdq = [(x[0], x[1], x[2], 12) for x in list(itertools.product(p, d, q))]

    # print('Examples of parameter combinations for Seasonal ARIMA...')
    # print('SARIMAX: {} x {}'.format(pdq[1], seasonal_pdq[1]))
    # print('SARIMAX: {} x {}'.format(pdq[1], seasonal_pdq[2]))
    # print('SARIMAX: {} x {}'.format(pdq[2], seasonal_pdq[3]))
    # print('SARIMAX: {} x {}'.format(pdq[2], seasonal_pdq[4]))

    warnings.filterwarnings("ignore") # specify to ignore warning messages
    for param in pdq:
        for param_seasonal in seasonal_pdq:
            try:
                mod = sm.tsa.statespace.SARIMAX(y,
                                                order=param,
                                                seasonal_order=param_seasonal,
                                                enforce_stationarity=False,
                                                enforce_invertibility=False)

                results = mod.fit()
                # print('ARIMA{}x{}12 - AIC:{}'.format(param, param_seasonal, results.aic)) # välj den kombo med minst AIC värde
            except:
                continue
def fit_time_series(y):
    warnings.filterwarnings("ignore") # specify to ignore warning messages

    mod = sm.tsa.statespace.SARIMAX(y,
                                    order=(1, 1, 1),
                                    seasonal_order=(1, 1, 1, 12),
                                    enforce_stationarity=False,
                                    enforce_invertibility=False)

    results = mod.fit()

    # print(results.summary().tables[1])
    # results.plot_diagnostics(figsize=(15, 12))
    return results
    # plt.show()
    #
def validate_forecast_non_dynamic(results, y):
    pred = results.get_prediction(start=pd.to_datetime('1998-01-01'), dynamic=False)
    pred_ci = pred.conf_int()

    ax = y['1990-01-01':].plot(label='observed')
    pred.predicted_mean.plot(ax=ax, label='One-step ahead Forecast', alpha=.7)

    ax.fill_between(pred_ci.index,
                    pred_ci.iloc[:, 0],
                    pred_ci.iloc[:, 1], color='k', alpha=.2)

    ax.set_xlabel('Date')
    ax.set_ylabel('CO2 Levels')
    plt.legend()

    plt.show()

    #average_error

    y_forecasted = pred.predicted_mean
    y_truth = y['1998-01-01':]

    # Compute the mean square error
    mse = ((y_forecasted - y_truth) ** 2).mean()
    print('The Mean Squared Error of our forecasts is {}'.format(round(mse, 2))) # Nära 0 är bra. 0 = perfect matchning mellan verklighet och forutspådd.

def validate_forecast_dynamic(results, y):
    pred_dynamic = results.get_prediction(start=pd.to_datetime('1998-01-01'), dynamic=True, full_results=True)
    pred_dynamic_ci = pred_dynamic.conf_int()
    print("hhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhe")
    print(y)
    print("hhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhe")
    ax = y['1990':].plot(label='observed', figsize=(20, 15))

    pred_dynamic.predicted_mean.plot(label='Dynamic Forecast', ax=ax)

    ax.fill_between(pred_dynamic_ci.index,
                    pred_dynamic_ci.iloc[:, 0],
                    pred_dynamic_ci.iloc[:, 1], color='k', alpha=.25)

    ax.fill_betweenx(ax.get_ylim(), pd.to_datetime('1998-01-01'), y.index[-1],
                     alpha=.1, zorder=-1)

    ax.set_xlabel('Date')
    ax.set_ylabel('CO2 Levels')

    plt.legend()
    plt.show()

    # Extract the predicted and true values of our time series
    y_forecasted = pred_dynamic.predicted_mean
    y_truth = y['1998-01-01':]

    # Compute the mean square error
    mse = ((y_forecasted - y_truth) ** 2).mean()
    print('The Mean Squared Error of our forecasts is {}'.format(round(mse, 2)))

def forecast_steps(results, y):
    # Get forecast 500 steps ahead in future
    # pred_uc = results.get_forecast(steps=500)
    # Get confidence intervals of forecasts
    
    start = datetime.datetime.strptime("2015-01-01 00:00:00", "%Y-%m-%d")
    date_list = pd.date_range('2015-01-01 00:00:00', freq='1H', periods=168)
    future = pd.DataFrame(index=date_list, columns= df.columns)
    data = pd.concat([results, future])
    
    
    pred = results.get_prediction(start=pd.to_datetime('2015-01-01'), dynamic=False)
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



data = sm.datasets.co2.load_pandas()
y = data.data
# The 'MS' string groups the data in buckets by start of the month and makes average for each month
y = y['co2'].resample('MS').mean()
# The term bfill means that we use the value before filling in missing values
y = y.fillna(y.bfill())

#print(y)
# y.plot(figsize=(15, 6))
# plt.show()
#parameter_selection_for_arima()
res = fit_time_series(y)
# validate_forecast_non_dynamic(res, y)
#validate_forecast_dynamic(res, y)
forecast_steps(res, y)
