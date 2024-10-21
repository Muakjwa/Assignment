import numpy as np

class Softmax_CE_loss():        
    def __init__(self):
        self.x = None
        self.t = None
        self.batch_size = None
        
    def forward(self, x, t, epsilone = 0.000001):
        self.x = x
        self.t = t
        #overflow 방지
        x_wo_of = self.x - np.max(self.x)
        output = np.exp(x_wo_of)/np.sum(np.exp(x_wo_of))
        self.batch_size = output.shape[0]
        loss = (np.sum(-1*self.t*np.log(output+epsilone)))/output.shape[0]
        return loss
    
    def prob(self,x):
        a= np.exp(5*x)/(np.array([np.sum(np.exp(5*x),axis =-1)]*x.shape[-1]).T)
        return a
    
    def backward(self):
        output = (self.x - self.t)/self.batch_size
        return output