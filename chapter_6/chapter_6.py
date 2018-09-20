import pandas as pd
from dateutil.relativedelta import relativedelta
import numpy as np
#import thread

class VSTOXXSubIndex:

    def __init__(self,path_to_subindexes):
        self.sub_index_store_path=path_to_subindexes
        self.utility=OptionUtility()
        self.webpage=EurexWebPage()
        self.calculator=VSTOXXCalculator()
        self.csv_date_format="%m/%d/%Y"

    def start(self,months=2,r=0.015):
        #For each date available, fetch the data
        for selected_date in self.webpage.get_available_dates():
            print("Collecting historical data for %s..."%selected_date)
            self.calculate_and_save_sub_indexes(selected_date,months,r)
        print("Completed")

    def calculate_and_save_sub_indexes(self,selected_date,months_fwd,r):
        current_dt=self.webpage.get_date_from_web_date(selected_date)

        for i in range(1,months_fwd+1):
            #Get settlement date of the expiring month
            expiry_dt=self.utility.fwd_expiry_date(current_dt,i)
            #Get calls and puts of expiringmonth
            dataset,update_dt=self.get_data(current_dt,expiry_dt)
            print(dataset)
            if not dataset.empty:
                sub_index=self.calculator.calculate_sub_index(dataset,update_dt,expiry_dt,r)
                self.save_vstoxx_sub_index_to_csv(current_dt,sub_index,i)

    def save_vstoxx_sub_index_to_csv(self,current_dt,sub_index,month):
        subindex_df=None
        try:
            subindex_df=pd.read_csv(self.sub_index_store_path,index_col=[0])
        except:
            subindex_df=pd.DataFrame()

        display_date=current_dt.strftime(self.csv_date_format)
        subindex_df.at[display_date,"I"+str(month)]=sub_index
        #subindex_df.set_value(display_date,"I"+str(month),sub_index)
        subindex_df.to_csv(self.sub_index_store_path)

    def get_data(self,current_dt,expiry_dt):
        """Fetch and join calls and puts option series data"""
        calls,dt1=self.webpage.get_option_series_data(True,current_dt,expiry_dt)
        puts,dt2=self.webpage.get_option_series_data(False,current_dt,expiry_dt)
        option_series=calls.join(puts,how='inner')
        if dt1!=dt2:
            print("Error:2 different underlyingprices.")
        return option_series,dt1
    
    
#----------------------------------------------
import calendar as cal
import datetime as dt

class OptionUtility(object):

    def get_settlement_date(self,date):
        """Get third friday of the month"""
        day=21-(cal.weekday(date.year,date.month,1)+2)%7
        return dt.datetime(date.year,date.month,day,12,0,0)

    def get_date(self,web_date_string,date_format):
        """Parse a date from the web to a date object"""
        return dt.datetime.strptime(web_date_string,date_format)

    def fwd_expiry_date(self,current_dt,months_fws):
        return self.get_settlement_date(current_dt+relativedelta(
            months=+months_fws))


#-------------------------------------
import urllib
from lxml import html

class EurexWebPage(object):

    def __init__(self):
        self.url="%s%s%s%s%s"%("http://www.eurexchange.com/",
                            "exchange-en/market-data/statistics/",
                            "market-statistics-online/180102!",
                            "onlineStats?productGroupId=846&productId=19068",
                            "&viewType=3")
        self.param_url="&cp=%s&year=%s&month=%s&busDate=%s"
        self.lastupdated_dateformat="%b %d, %Y %H:%M:%S"
        self.web_date_format="%Y%m%d"
        self.__strike_price_header__="Strike price"
        self.__prices_header__="Daily settlem. price"
        self.utility=OptionUtility()

    def get_available_dates(self):
        from urllib.request import Request,urlopen
        req=Request(self.url,headers={'User-Agent': 'Mozilla/5.0'})
        html_data=urlopen(req).read()
        webpage=html.fromstring(html_data)
        #html_data=urllib.request.urlopen(self.url).read()
        #webpage=html.fromstring(html_data)
        #find the dates available on the website
        dates_listed=webpage.xpath("//select[@name='busDate']"+"/option")

        return [date_element.get("value") for date_element in
                reversed(dates_listed[0:-1])]

    def get_date_from_web_date(self,web_date):
        return self.utility.get_date(web_date,self.web_date_format)

    def get_option_series_data(self,is_call,current_dt,option_dt):
        from urllib.request import Request,urlopen
        selected_date=current_dt.strftime(self.web_date_format)
        option_type="Call" if is_call else "Put"
        target_url=(self.url+self.param_url)%(option_type,option_dt.year,option_dt.month,selected_date)
        ##########
        req=Request(target_url,headers={'User-Agent':'Mozilla/5.0'})
        html_data=urlopen(req).read()
        webpage=html.fromstring(html_data)
        
        '''
        opener = urllib.request.build_opener()
        opener.addheaders = [('User-agent', 'Mozilla/5.0')]
        f=opener.open(target_url)
        f.read()
        ''' 
        #html_data=urllib.urlopen(target_url).read()
        #webpage=html.fromstring(html_data)
        update_date=self.get_last_update_date(webpage)
        indexes=self.get_data_headers_indexes(webpage)
        data=self.__get_data_rows__(webpage,indexes,option_type)
        return data, update_date

    def __get_data_rows__(self,webpage,indexes,header):
        data=pd.DataFrame()
        for row in webpage.xpath("//table[@class='dataTable']/"+"tbody/tr"):
            columns=row.xpath("./td")
            if len(columns)>max(indexes):
                try:
                    [K,price]=[float(columns[i].text.replace(",","")) for i in indexes]
                    #data.set_value(K,header,price)
                    data.at[K,header]=price
                except:
                    continue
        return data

    def get_data_headers_indexes(self,webpage):
        table_headers=webpage.xpath("//table[@class='dataTable']"+"/thead/th/text()")
        indexes_of_interest=[table_headers.index(self.__strike_price_header__),
                             table_headers.index(self.__prices_header__)]
        return indexes_of_interest

    def get_last_update_date(self,webpage):
        return dt.datetime.strptime(webpage.xpath("//p[@class='date']/b")[-1].text,
                                    self.lastupdated_dateformat)

    

#-----------------------------
import math
class VSTOXXCalculator(object):

    def __init__(self):
        self.secs_per_day=float(60*60*24)
        self.secs_per_year=float(365*self.secs_per_day)

    def calculate_sub_index(self,df,t_calc,t_settle,r):
        T=(t_settle-t_calc).total_seconds()/self.secs_per_year
        R=math.exp(r*T)

        # Calculate dK
        df["dK"]=0
        df["dK"][df.index[0]]=df.index[1]-df.index[0]
        df["dK"][df.index[-1]]=df.index[-1]-df.index[-2]
        df["dK"][df.index[1:-1]]=(df.index.values[2:]-df.index.values[:-2])/2

        #Calculate the forward price
        df["AbsDiffCP"]=abs(df["Call"]-df["Put"])
        min_val=min(df["AbsDiffCP"])
        f_df=df[df["AbsDiffCP"]==min_val]
        fwd_prices=f_df.index+R*(f_df["Call"]-f_df["Put"])
        F=np.mean(fwd_prices)

        #Get the strike not exceeding forward price
        K_i0=df.index[df.index<=F][-1]

        #Calculate M(K(i,j))
        df["MK"]=0
        df["MK"][df.index<K_i0]=df["Put"]
        df["MK"][K_i0]=(df["Call"][K_i0]+df["Put"][K_i0])/2.
        df["MK"][df.index>K_i0]=df["Call"]
        # Apple the variance formula to get the sub_index
        summation=sum(df["dK"]/(df.index.values**2)*R*df["MK"])
        variance=2/T*summation-1/T*(F/float(K_i0)-1)**2
        subindex=100*math.sqrt(variance)
        return subindex
    

        

if __name__=="__main__":
    import sys
    pathsave="E:/python_study/Mastering_Python_for_finance/chapter_6"
    sys.path.append(pathsave)
    vstoxx_subindex=VSTOXXSubIndex(pathsave+"/data/vstoxx_sub_indexes.csv")
    vstoxx_subindex.start(2)
    
 

















