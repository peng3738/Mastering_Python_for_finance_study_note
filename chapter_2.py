from scipy import stats

#stock return and market index return 
stock_returns=[0.065,0.0265,-0.0593,-0.001,0.0346]
mkt_returns=[0.055,-0.09,-0.041,0.045,0.022]
#------------------
"""capm """
beta,alpha,r_value,p_value,std_err=stats.linregress(stock_returns,mkt_returns)
print(beta,alpha)
#----------------------
"""Calculating the sml """
rf=0.05
mrisk_prem=0.085
#
risk_prem=mrisk_prem*beta
expected_stock_return=rf+risk_prem
print('expected stock return:', expected_stock_return)
#-----------------------------
"""APT"""
""" Least squares regression with statsmodels """
import numpy as np
import statsmodels.api as sm
import random
random.seed(12345)
num_periods=9
all_values=np.array([np.random.random(8) for i in range (num_periods)])
y_values=all_values[:,0]
x_values=all_values[:,1:]
x_values=sm.add_constant(x_values)# Include the intercept
results=sm.OLS(y_values,x_values).fit() # Regress and fit the model
print(results.summary())
print(results.params)

#----------------------------------
""" A simple linear optimization problem with 2 variables """
import pulp
x=pulp.LpVariable("x",lowBound=0)
y=pulp.LpVariable("y",lowBound=0)

problem=pulp.LpProblem("A simple maximization objective",
                       pulp.LpMaximize)
problem+=3*x+2*y,"The objective function "
problem+=2*x+y<=100,"1st construction"
problem+=x+y<=80,"2nd constraint"
problem+=x<=40,"3rd constraint"
problem.solve()
print("Maximization Results:")
for variable in problem.variables():
    print(variable.name, "=", variable.varValue)

#----------------------------
""" An example of implementing an IP model with binary conditions  """

import pulp
dealers=["X","Y","Z"]
variable_costs={"X":500,"Y":350,"Z":450}
fixed_costs={"X":4000,"Y":2000,"Z":6000}
#define PuLP variables to solve
quantities=pulp.LpVariable.dicts("quantity",dealers,lowBound=0,cat=pulp.LpInteger)
is_orders=pulp.LpVariable.dicts("orders",dealers,cat=pulp.LpBinary)

"""

This is an example of implementing an IP model with binary

variables the correct way.

"""

# Initialize the model with constraints
model=pulp.LpProblem("A cost minimization problem",pulp.LpMinimize)
model+=sum([variable_costs[i]*quantities[i]+
            fixed_costs[i]*is_orders[i] for i in dealers ]),\
            "Minimize portfolio cost"
model+=sum([quantities[i] for i in dealers])==150,\
        "Total contracts required"
model+=is_orders["X"]*30<=quantities["X"]<=\
        is_orders["X"]*100,"Boundary of total volume of X"
model+=is_orders["Y"]*30<=quantities["Y"]<=\
        is_orders["Y"]*90,"Boundary of total volume of Y"
model+=is_orders["Z"]*30<=quantities["Z"]<=\
        is_orders["Z"]*70,"Boundary of total volume of Z"
model.solve()

print("Minimization results:")
for variable in model.variables():
    print(variable,"=",variable.varValue)

print("Total cost:%s"%pulp.value(model.objective))

#------------------------------------------------------
"""Linear algebra with numpy matrices"""
import numpy as np
A=np.array([[2,1,1],[1,3,2],[1,0,0]])
B=np.array([4,5,6])
print(np.linalg.solve(A,B))
#------------------------------------
"""LU decomposition with Scipy"""
import scipy.linalg as linalg
import numpy as np
A=np.array([[2.,1.,1.],[1.,3.,2.],[1.,0.,0.]])
B=np.array([4.,5.,6.])

LU=linalg.lu_factor(A)
x=linalg.lu_solve(LU,B)

print(x)
#----------------------
P,L,U=linalg.lu(A)
list(L)
list(U)
#----------------------------------
"""Cholesky decomposition with Numpy"""
import numpy as np
A=np.array([[10.,-1.,2.,0.],[-1.,11.,-1.,3.],
            [2.,-1.,10.,-1.],[0.0,3.,-1.,8.]])
B=np.array([6.,25.,-11.,15.])
L=np.linalg.cholesky(A)
print(L)

print(np.dot(L,L.T.conj()))
y=np.linalg.solve(L,B)
x=np.linalg.solve(L.T.conj(),y)
print(x)
print(np.mat(A)*np.mat(x).T)

#-------------------------------
"""QR decomposition with scipy"""
import scipy.linalg as linalg
import numpy as np

A=np.array([[2.,1.,1.],[1.,3.,2.],[1.,0.,0]])
B=np.array([4.,5.,6.])
Q,R=linalg.qr(A)
y=np.dot(Q.T,B)
x=linalg.solve(R,y)
print(x)

#---------------------------------
"""Solve Ax=B with the Jacobi method"""
import numpy as np
def jacobi(A,B,n,tol=1e-10):
    #Initializes x with zeros with same shape and type as B
    x=np.zeros_like(B)
    for it_count in range(n):
        x_new=np.zeros_like(x)
        for i in range(A.shape[0]):
            s1=np.dot(A[i,:i],x[:i])
            s2=np.dot(A[i,i+1:],x[i+1:])
            x_new[i]=(B[i]-s1-s2)/A[i,i]
        if np.allclose(x,x_new,tol):
            break
        x=x_new
    return x

A=np.array([[10.,-1.,2.,0.],[-1.,11.,-1.,3.],
            [2.,-1.,10.,-1.],[0.0,3.,-1.,8.]])
B=np.array([6.,25.,-11.,15.])
n=25
x=jacobi(A,B,n)
print("x=",x)

#---------------------------------------
""" solve Ax=B with the gauss seidel method"""
import numpy as np
def gauss(A,B,n,tol=1e-10):
    L=np.tril(A)
    U=A-L#decompose A=L+U
    L_inv=np.linalg.inv(L)
    x=np.zeros_like(B)
    
    for i in range(n):
        Ux=np.dot(U,x)
        x_new=np.dot(L_inv,B-Ux)

        if np.allclose(x,x_new,tol):
            break
        
        x=x_new
        
    return x

A=np.array([[10.,-1.,2.,0.],[-1.,11.,-1.,3.],
            [2.,-1.,10.,-1.],[0.0,3.,-1.,8.]])
B=np.array([6.,25.,-11.,15.])
n=100
x=gauss(A,B,n)
print("x=",x)










