"""Price a European option by the implicit method of finite difference"""
import numpy as np
import scipy.linalg as linalg

from FDExplicitEu import FDExplicitEu

class FDImplicitEu(FDExplicitEu):

    def _setup_coefficients_(self):
        self.a=0.5*(self.r*self.dt*self.i_values-
                    (self.sigma**2)*self.dt*(self.i_values**2))
        self.b=1+(self.sigma**2)*self.dt*(self.i_values**2)+self.r*self.dt
        self.c=-0.5*(self.r*self.dt*self.i_values+
                     (self.sigma**2)*self.dt*(self.i_values**2))
        self.coeffs=np.diag(self.a[2:self.M],-1)+np.diag(self.b[1:self.M])+\
                     np.diag(self.c[1:self.M-1],1)
        #print(self.coeffs)
        #print(self.coeffs.shape)

    def _traverse_grid_(self):
        """Solve using linear systems of equations"""
        P,L,U=linalg.lu(self.coeffs)
        aux=np.zeros(self.M-1)
        cux=np.zeros(self.M-1)

        for j in reversed(range(self.N)):
            aux[0]=np.dot(-self.a[1],self.grid[0,j])
            cux[-1]=np.dot(-self.c[-1],self.grid[self.M,j])
            x1=linalg.solve(L,self.grid[1:self.M,j+1]+aux+cux)
            x2=linalg.solve(U,x1)
            self.grid[1:self.M,j]=x2
        

#-------------------------------------
if __name__=="__main__":
    from FDImplicitEu import FDImplicitEu
    options=FDImplicitEu(50,50,0.1,5./12.,0.4,100,100,1000,False)
    print(options.price())

    options=FDImplicitEu(50,50,0.1,5./12.,0.4,100,100,100,False)
    print(options.price())
    