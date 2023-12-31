# -*- coding: utf-8 -*-
"""arima_model_traffic_prediction.ipynb

Automatically generated by Colaboratory.

Original file is located at
    https://colab.research.google.com/drive/1sA-qWRlnvz-zbESl1n1dbdWPpAEoJeX5
"""

pip install pmdarima

import pandas as pd
import numpy as np
import matplotlib.pyplot as plt

"""Read Data"""

df=pd.read_csv("/content/traffic.csv",parse_dates=['DateTime'],index_col='DateTime',infer_datetime_format=True)
print('Shape of data', df.shape)

"""Dropping the unwanted columns"""

df.drop(['ID','Junction'],axis=1,inplace=True)

"""Taking the observations from 1 to 1000

"""

df=df[1:1000]
df=df.dropna()
df.head()

df.tail()

"""Visualising the data"""

df['Vehicles'].plot()

"""P-value check"""

from statsmodels.tsa.stattools import adfuller
def ad_test(dataset):
  dftest = adfuller(dataset, autolag = 'AIC')
  print("1. ADF : ",dftest[0])
  print("2. P-value : ", dftest[1])
  print("3. Num of Lags : ", dftest[2])
  print("4. Num of observations used for ADF Regression:", dftest[3])
  print("5. Critical values : ")
  for key, val in dftest[4].items():
         print("\t",key, ": ", val)

ad_test(df['Vehicles'])

"""Differencing the data as p>0.05"""

df_diff = df.diff().dropna()

df_diff.head()

"""Differenced data"""

plt.plot(df_diff)

"""Ad fuller test to check the p-value again"""

from statsmodels.tsa.stattools import adfuller
def ad_test(dataset):
  dftest = adfuller(dataset, autolag = 'AIC')
  print("1. ADF : ",dftest[0])
  print("2. P-value : ", dftest[1])
  print("3. Num of Lags : ", dftest[2])
  print("4. Num of observations used for ADF Regression:", dftest[3])
  print("5. Critical values : ")
  for key, val in dftest[4].items():
         print("\t",key, ": ", val)

ad_test(df_diff['Vehicles'])

"""Ignoring the warnings"""

from pmdarima import auto_arima
import warnings
warnings.filterwarnings("ignore")

"""Finding the best model"""

from pmdarima import auto_arima
stepwise_fit = auto_arima(df_diff['Vehicles'], trace=True,
suppress_warnings=True)
stepwise_fit.summary()

"""Training the model"""

from statsmodels.tsa.arima_model import ARIMA

print(df_diff.shape)
train=df_diff.iloc[:-50]
test=df_diff.iloc[-50:]
print(train.shape,test.shape)
train.head()

"""Fitting the model"""

import statsmodels.api as sm

model= sm.tsa.arima.ARIMA(train["Vehicles"],order=(3,0,2))
model=model.fit()
model.summary()

"""Plotting the model"""

start=len(train)
end=len(train)+len(test)-1
pred=model.predict(start=start,end=end,typ='levels').rename('ARIMA Predictions')
pred.plot(legend=True)
test['Vehicles'].plot(legend=True)

"""Error calculation"""

from sklearn.metrics import mean_squared_error
from math import sqrt
test['Vehicles'].mean()
rmse=sqrt(mean_squared_error(pred,test['Vehicles']))
print(rmse)

index_future_dates=pd.date_range(start='2015-11-01',end='2015-12-12')
pred=model.predict(start=len(df),end=len(df)+50,typ='levels').rename('ARIMA Predictions')
print(pred)

pred.plot(figsize=(12,5), legend=True)

"""# New Section

# New Section
"""

