"""Price a europeann option by the binomial tree model"""
import sys
path="E:\python_study\Mastering_Python_for_finance"
sys.path.append(path)

from StockOption import StockOption
import math
import numpy as np

class BinomialEuropeanOption(StockOption):

    def __setup_parameters__(self):
        """reauired calculations for the model"""
        self.M=self.N+1
        self.u=1+self.pu
        self.d=1-self.pd
        self.qu=(math.exp((self.r-self.div)*self.dt)-self.d)/(self.u-self.d)
        self.qd=1-self.qu

    def _initialize_stock_price_tree_(self):
        #initialize terminal prices nodes to zeros
        self.STs=np.zeros(self.M)
        #calculate expected stock prices for each node
        for i in range(self.M):
            self.STs[i]=self.S0*(self.u**(self.N-i))*(self.d**i)

    def _initialize_payoffs_tree_(self):
        #get payoffs when the option expires at terminal nodes
        payoffs=np.maximum(0,(self.STs-self.K) if self.is_call else (self.K-self.STs))
        return payoffs

    def _traverse_tree_(self,payoffs):
        #Starting from the time the option expires, traverse
        #backwards and calculate discounted payoffs at each node
        for i in range(self.N):
            payoffs=(payoffs[:-1]*self.qu+payoffs[1:]*self.qd)*self.df
        return payoffs

    def __begin_tree_traversal__(self):
        payoffs=self._initialize_payoffs_tree_()
        return self._traverse_tree_(payoffs)

    def price(self):
        """The pricing implementation"""
        self.__setup_parameters__()
        self._initialize_stock_price_tree_()
        payoffs=self.__begin_tree_traversal__()

        return payoffs[0]
    


if __name__ == "__main__":
    from BinomialEuropeanOption import BinomialEuropeanOption
    eu_option = BinomialEuropeanOption(
        50, 50, 0.05, 0.5, 2,
        {"pu": 0.2, "pd": 0.2, "is_call": False})
    print(eu_option.price())













    
            
