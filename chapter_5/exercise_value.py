import math
import numpy as np

def exercise_value(K,R,t):
    return K*math.exp(-R*t)

#----------------------------------
if __name__=="__main__":
    from exact_zcb import exact_zcb 
    Ts=np.r_[0.0:25.5:0.5]
    Ks=[exercise_value(0.95,0.015,t) for t in Ts]

    zcbs=[exact_zcb(0.5,0.02,0.03,t,0.015) for t in Ts]
    import matplotlib.pyplot as plt
    plt.title("Zero Coupon Bond (ZCB) and Strike (K) Values by Time")
    plt.plot(Ts,zcbs,label='ZCB')
    plt.plot(Ts,Ks,label='K',linestyle="--",marker=".")
    plt.ylabel("Value ($)")
    plt.xlabel("Time in years")
    plt.legend()
    plt.grid(True)
    plt.show()

    
