'''
from lxml import html
import urllib

months=2
r=0.015
url="%s%s%s%s%s"%("http://www.eurexchange.com/",
                            "exchange-en/market-data/statistics/",
                            "market-statistics-online/180102!",
                            "onlineStats?productGroupId=846&productId=19068",
                            "&viewType=3")
param_url="&cp=%s&year=%s&month=%s&busDate=%s"
lastupdated_dateformat="%b %d, %Y %H:%M:%S"
web_date_format="%Y%m%d"
__strike_price_header__="Strike price"
__prices_header__="Daily settlem. price"

from urllib.request import Request,urlopen
req=Request(url,headers={'User-Agent': 'Mozilla/5.0'})
html_data=urlopen(req).read()
webpage=html.fromstring(html_data)
dates_listed=webpage.xpath("//select[@name='busDate']"+"/option")

get_available_dates=[date_element.get("value") for date_element
                     in reversed(dates_listed[0:-1])]

selected_date=get_available_dates[0]
print("Collecting historical data for %s..."%selected_date)

months_fwd=months

import calendar as cal
import datetime as dt

web_date=selected_date
current_dt=dt.datetime.strptime(web_date,web_date_format)
#------------------------
from dateutil.relativedelta import relativedelta
i=2
months_fws=i
date=current_dt+relativedelta(months=+months_fws)
day=21-(cal.weekday(date.year,date.month,1)+2)%7
expiry_dt=dt.datetime(date.year,date.month,day,12,0,0)

print(expiry_dt)
print(current_dt)

is_call=True

from urllib.request import Request,urlopen
selected_date=current_dt.strftime(web_date_format)
option_type="Call" if is_call else "Put"
target_url=(url+param_url)%(option_type,option_dt.year,option_dt.month,selected_date)

'''

import pandas as pd
pathsave='E:/python_study/Mastering_Python_for_finance/chapter_6/data/'
vstoxx_sub_indexes=pd.read_csv(pathsave+'vstoxx_sub_indexes.csv',index_col=[0],parse_dates=True,dayfirst=False)
columns=['V2TX', 'V6I1', 'V6I2', 'V6I3', 'V6I4', 'V6I5', 'V6I6', 'V6I7', 'V6I8']
vstoxx=pd.read_csv(pathsave+'vstoxx.txt',index_col=[0],names=columns,parse_dates=True,skiprows=3,dayfirst=True)
#vstoxx.set_index('Date')
start_dt=min(vstoxx_sub_indexes.index.values)
vstoxx=vstoxx[vstoxx.index>=start_dt]
from pylab import *
new_pd=pd.DataFrame(vstoxx_sub_indexes["I2"])
#new_pd=new_pd.join(vstoxx["V6I2"],how='inner')
new_pd.plot(figsize=(10,6),grid=True)
















