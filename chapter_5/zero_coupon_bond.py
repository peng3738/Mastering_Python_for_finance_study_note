#----------------------
"""zero coupon bond"""
def zero_coupon_bond(par,r,t):
    """
    Price a zero coupon bond.
    Par- face value of the bond
    r -annual yield or rate of the bond
    t -time to maturity in years
    """
    return par/(1+r)**t
#----------------------------
print(zero_coupon_bond(100,0.05,5))

#-----------------------------
