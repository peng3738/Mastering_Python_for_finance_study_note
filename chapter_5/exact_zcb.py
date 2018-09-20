"""Get zero coupon bond price by Vasicek model"""
import numpy as np
def exact_zcb(theta,kappa,sigma,tau,r0=0.):
    B=(1-np.exp(-kappa*tau))/kappa
    A=np.exp((theta-(sigma**2)/(2*(kappa**2)))*(B-tau)-
             (sigma**2)/(4*kappa)*(B**2))
    return A*np.exp(-r0*B)

#----------------------
if __name__=="__main__":
    Ts=np.r_[0.0:25.5:0.5]
    zcbs=[exact_zcb(0.5,0.02,0.03,t,0.015) for t in Ts]

    import matplotlib.pyplot as plt
    plt.title("Zero Coupon Bond values by Time")
    plt.plot(Ts,zcbs,label='ZCB')
    plt.ylabel("Values ($)")
    plt.xlabel("Time in years")
    plt.legend()
    plt.grid(True)
    plt.show()

    
                    

