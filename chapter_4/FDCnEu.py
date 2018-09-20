"""Crank_Nicolson method of finite Differences"""
import numpy as np
import scipy.linalg as linalg
from FDExplicitEu import FDExplicitEu

class FDCnEu(FDExplicitEu):

    def _setup_coefficients_(self):
        self.alpha=0.25*self.dt*((self.sigma**2)*(self.i_values**2)-
                                 self.r*self.i_values)
        self.beta=-0.5*self.dt*((self.sigma**2)*(self.i_values**2)+self.r)
        self.gamma=0.25*self.dt*((self.sigma**2)*(self.i_values**2)+
                                 self.r*self.i_values)

        self.M1=-np.diag(self.alpha[2:self.M],-1)+np.diag(1-self.beta[1:self.M])-\
                 np.diag(self.gamma[1:self.M-1],1)

        self.M2=np.diag(self.alpha[2:self.M],-1)+np.diag(1+self.beta[1:self.M])+\
                 np.diag(self.gamma[1:self.M-1],1)

    def _traverse_grid_(self):
        """Solve using linear systems of equations"""
        P,L,U=linalg.lu(self.M1)
        aux=np.zeros(self.M-1)
        cux=np.zeros(self.M-1)
        

        for j in reversed(range(self.N)):
            aux[0]=np.dot(self.alpha[1],self.grid[0,j]+self.grid[0,j+1])
            cux[-1]=np.dot(self.gamma[-1],self.grid[self.M,j]+self.grid[self.M,j+1])
            x1=linalg.solve(L,np.dot(self.M2,self.grid[1:self.M,j+1]+aux+cux))
            x2=linalg.solve(U,x1)
            self.grid[1:self.M,j]=x2

#------------------------------------
if __name__=="__main__":
    from FDCnEu import FDCnEu
    options=FDCnEu(50,50,0.1,5./12.,0.4,100,100,1000,False)
    print(options.price())

    options=FDCnEu(50,50,0.1,5./12.,0.4,100,100,100,False)
    print(options.price())   


        

