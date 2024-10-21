import numpy as np

class tanh():
    def forward(self, x):
        return (1-np.exp(-2*x))/(1+np.exp(-2*x))
    
    def backward(self, x):
        return 1-self.forward(x)**2
    
class sigmoid():
    def forward(self, x):
        return np.exp(x)/(np.exp(x)+1)
    
    def backward(self, x):
        return x*(1-x)