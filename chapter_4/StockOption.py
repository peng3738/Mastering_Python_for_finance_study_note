"""Store common attributes of a stock option"""
import math

class StockOption(object):

    def __init__(self,S0,K,r,T,N,params):
        self.S0=S0
        self.K=K
        self.r=r
        self.T=T
        self.N=max(1,N)
        self.STs=None

        """Optional parameters used by derived classes"""
        self.pu=params.get("pu",0)#probability of up state
        self.pd=params.get("pd",0)#probability of down state
        self.div=params.get("div",0)#dividend yield
        self.sigma=params.get("sigma",0)#volatility
        self.is_call=params.get("is_call",True)# call or put
        self.is_european=params.get("is_eu",True)#Eu or Am

        """computed values"""
        self.dt=T/float(N)
        self.df=math.exp(-(r-self.div)*self.dt)

