"""Ger bond price frim YTM"""
def bond_price(par,T,ytm,coup,freq=2):
    freq=float(freq)
    periods=T*freq
    coupon=coup/100.*par/freq
    dt=[(i+1)/freq for i in range(int(periods))]
    price=sum([coupon/(1+ytm/freq)**(freq*t) for t in dt])+\
           par/(1+ytm/freq)**(freq*T)
    return price
#------------------------
if __name__=="__main__":
    ytm=0.09369155345239522
    print(bond_price(100,1.5,ytm,5.75,2))
    
