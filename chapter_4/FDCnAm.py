"""Price an American option by the Crank-Nicolson method"""
import numpy as np
import sys

from FDCnEu import FDCnEu

class FDCnAm(FDCnEu):

    def __init__(self,S0,K,r,T,sigma,Smax,M,N,omega,tol,is_call=True):
        super(FDCnAm,self).__init__(S0,K,r,T,sigma,Smax,M,N,is_call)
        self.omega=omega
        self.tol=tol
        self.i_values=np.arange(self.M+1)
        self.j_values=np.arange(self.N+1)

    def _setup_boundary_conditions_(self):
        if self.is_call:
            self.payoffs=np.maximum(self.boundary_conds[1:self.M]-self.K,0)
            self.upconds=np.zeros(self.N+1)
            self.downconds=self.Smax-self.K*np.exp(-self.r*self.dt*
                                                        (self.N-self.j_values))
        else:
            self.payoffs=np.maximum(self.K-self.boundary_conds[1:self.M],0)
            self.upconds=self.K*np.exp(-self.r*self.dt*(self.N-self.j_values))
            self.downconds=np.zeros(self.N+1)
            
        self.past_values=self.payoffs
       # self.boundary_values=self.K*np.exp(-self.r*self.dt*(self.N-self.j_values))

    def _traverse_grid_(self):
        """Solve using linear systems of equations"""
        aux=np.zeros(self.M-1)
        cux=np.zeros(self.M-1)
        new_values=np.zeros(self.M-1)

        for j in reversed(range(self.N)):
            #print(self.alpha[1])
            #print(j)
            #print(self.upconds.shape)
            #print(self.upconds)
            #print(self.upconds[j+1])
            aux[0]=self.alpha[1]*(self.upconds[j]+self.upconds[j+1])
            cux[-1]=self.gamma[-1]*(self.downconds[j]+self.downconds[j+1])
            rhs=np.dot(self.M2,self.past_values)+aux+cux
            old_values=np.copy(self.past_values)
            error=sys.float_info.max

            while self.tol<error:
                new_values[0]=max(self.payoffs[0],old_values[0]+
                                  self.omega/(1-self.beta[1])*
                                  (rhs[0]-(1-self.beta[1])*old_values[0]+
                                   (self.gamma[1]*old_values[1])))

                for k in range(self.M-2)[1:]:
                    new_values[k]=max(self.payoffs[k],old_values[k]+
                            self.omega/(1-self.beta[k+1])*(rhs[k]+
                            self.alpha[k+1]*new_values[k-1]-
                            (1-self.beta[k+1])*old_values[k]+
                            self.gamma[k+1]*old_values[k+1]))
                    
                new_values[-1]=max(self.payoffs[-1],old_values[-1]+
                                  self.omega/(1-self.beta[-2])*
                                  (rhs[-1]+self.alpha[-2]*new_values[-2]-
                                   (1-self.beta[-2])*old_values[-1]))

                error=np.linalg.norm(new_values-old_values)
                old_values=np.copy(new_values)
                
            self.past_values=np.copy(new_values)

        self.values=np.concatenate(([self.upconds[0]],new_values,
                                    [self.downconds[-1]]))

    def _interpolate_(self):
        #use linear interpolation on final values as 1D array
        return np.interp(self.S0,self.boundary_conds,self.values)

#------------------------------------------
if __name__=="__main__":
    from FDCnAm import FDCnAm
    options=FDCnAm(50,50,0.1,5./12.,0.4,100,100,42,1.2,0.001)
    print(options.price())

    options=FDCnAm(50,50,0.1,5./12.,0.4,100,100,42,1.2,0.001,False)
    print(options.price())   
    
























            
            
