#-----------------------------
"""Incremental_search"""
import numpy as np

def incremental_search(f,a,b,dx):
    """
    :param f: the function to solve
    :param a : the left boundary x-axis value
    :param b:the right bounday x-axis value
    :param dx: the incremental value in searching
    :return: the x-axis value of the root number of iterations used
    """
    fa=f(a)
    c=a+dx
    fc=f(c)
    n=1

    while np.sign(fa)==np.sign(fc):
        if a>=b:
            return a-dx,n
        a=c
        fa=fc
        c=a+dx
        fc=f(c)
        n+=1

    if fa==0:
        return a,n
    elif fc==0:
        return c,n
    else:
        return (a+c)/2.,n

#---------------------------
y=lambda x: x**3+2.*x**2-5.
root,iterations=incremental_search(y,-5.,5.,0.001)
print("Root is:" ,root)
print("Iterations:",iterations)

#--------------------------
"""The bisection method"""
def bisection(f,a,b,tol=0.1,maxiter=10):
    """
    :param f: the function to solve
    :param a: the x axis value where f(a)<0
    :param b: the x axis value where f(b)>0
    :param tol: the precision of the solution
    :param maxiter:maximum number of iterations
    :return: the x-axis value of the root,number of iterations used
    """
    c=(a+b)/2
    n=1
    while n<=maxiter:
        c=(a+b)/2
        if f(c)==0 or abs(a-b)/2<tol:
            return c,n

        n+=1
        if f(c)<0:
            a=c
        else:
            b=c
#--------------------------------
y=lambda x: x**3+2*x**2-5
root,iterations=bisection(y,-5,5,0.00001,100)
print("Root is:" ,root)
print("Iterations:",iterations)

#--------------------------
"""The newton method"""
def Newton(f,df,x,tol=0.001,maxiter=100):
    """
    :param f: The function to solve
    :param df: the derivative function of f
    :param x: Initial guess value of x
    :param tol:the precision of the solution
    :param maxiter: Maximum number of iterations
    :return: the x-axis value of the root,number of iterations used
    """
    n=1
    while n<=maxiter:
        x1=x-f(x)/df(x)
        if abs(x1-x)<tol:
            return x1,n
        else:
            x=x1
            n+=1
    return None,n
#----------------------------
y=lambda x:x**3+2*x**2-5
dy=lambda x:3*x**2+4*x
root,iterations=Newton(y,dy,5.0,0.00001,100)
print("Root is:" ,root)
print("Iterations:",iterations)

#-----------------------
"""The secant root finding method"""
def secant(f,a,b,tol=0.001,maxiter=100):
    """
    : param f : the function to solve
    : param a: initial x-axis guess value
    : param b: initial x-axis guess value, where b>a
    : param tol: the precision of the solution 
    : param maxiter: maximum number of iteratios
    : return: the x-axis value of the root, number of iterations used 

    """
    n=1
    while n<=maxiter:
        c=b-f(b)*(b-a)/(f(b)-f(a))
        if abs(c-b)<tol:
            return c,n
        a=b
        b=c
        n+=1
    return none, n
#-------------------------------
y=lambda x:x**3+2*x**2-5
root,iterations=secant(y,-5.,5.0,0.00001,100)
print("Root is:" ,root)
print("Iterations:",iterations)
        

#---------------------------------
"""
Documentation at
http://docs.scipy.org/doc/scipy/reference/optimize.html
"""
import scipy.optimize as optimize
y=lambda x:x**3+2*x**2-5
dy=lambda x:3*x**2+4*x

#call method: bisect(f,a,b [,args,xtol,rtol,maxiter,...])
print("Bisection method:%s"%optimize.bisect(y,-5.,5.,xtol=0.00001))
#call method: newton(func,x0,[,fprime,args,tol,...])
print("Newton's method:%s"%optimize.newton(y,5.,fprime=dy))
#when fprime-None,then the secant method is used
print("Secant method :%s"%optimize.newton(y,5.))
#call method: brentq(f,a,b,[,args,xtol,rtol,maxiter,...])
print("Brent's method:%s"%optimize.brentq(y,-5.,5.))

#----------------------------------
"""
General nonlinear solvers
- with a solution
"""
import scipy.optimize as optimize

y = lambda x: x**3 + 2.*x**2 - 5.
dy = lambda x: 3.*x**2 + 4.*x

print(optimize.fsolve(y, 5., fprime=dy))
print(optimize.root(y, 5.))


#---------------------------------
"""
General nonlinear solvers
- with no solution
"""


import scipy.optimize as optimize

y = lambda x: x**3 + 2.*x**2 - 5.
dy = lambda x: 3.*x**2 + 4.*x

print(optimize.fsolve(y, -5., fprime=dy))
print(optimize.root(y, -5.))






































    
    
