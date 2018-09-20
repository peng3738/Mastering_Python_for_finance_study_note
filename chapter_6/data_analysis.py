import pandas as pd

data_folder='E:/python_study/Mastering_Python_for_finance/chapter_6/'
stoxxeu600_filepath=data_folder+"stoxxeu600.txt"
vstoxx_filepath=data_folder+"vstoxx.txt"

columns=['Date','SX5P','SX5E','SXXP','SXXE','SXXF','SXXA','DK5F','DKXF','EMPTY']
#result=pd.read_table(stoxxeu600_filepath)
stoxxeu600=pd.read_csv(stoxxeu600_filepath,index_col=0,parse_dates=True,
                    dayfirst=True,header=None,skiprows=4,names=columns,sep=';')
del stoxxeu600['EMPTY']

stoxxeu600.info()

vstoxx=pd.read_csv(vstoxx_filepath,index_col=0,parse_dates=True,dayfirst=True,
                   header=2)
vstoxx.info()

import datetime as dt

cutoff_date=dt.datetime(1999,1,4)
data=pd.DataFrame({'EUROSTOXX':stoxxeu600['SX5E'][stoxxeu600.index>=cutoff_date],
                   'VSTOXX':vstoxx['V2TX'][vstoxx.index>=cutoff_date]})
data=data.dropna()
data=data[data>0]

data.info()

data.head()

from pylab import *
data.plot(subplots=True,figsize=(10,8),color="blue",grid=True)
show()

data.diff().hist(figsize=(10,5),color='blue',bins=100)

import numpy as np
log_returns=np.log(data/data.shift(1)).dropna()
log_returns.plot(subplots=True,figsize=(10,8),color='blue',grid=True)
show()

log_returns.corr()

import statsmodels.api as sm

log_returns.plot(figsize=(10,8),x="EUROSTOXX",y="VSTOXX",kind='scatter')
ols_fit=sm.OLS(log_returns['VSTOXX'].values,log_returns['EUROSTOXX'].values).fit()

plot(log_returns['EUROSTOXX'],ols_fit.fittedvalues,'r')

log_returns['EUROSTOXX'].rolling(window=252).corr(log_returns['VSTOXX']
                ).plot(figsize=(10,8))

plt.ylabel('Rolling Annual Correlation')
plt.show()

















