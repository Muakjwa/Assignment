import numpy as np

class Softmax_CE_loss():        
    def __init__(self, epsilone = 0.000001):
        self.x = None
        self.t = None
        self.batch_size = None
        self.epsilone = epsilone
        
    def forward(self,x,t):
        self.x = x
        self.t = t
        #overflow 방지
        x_wo_of = self.x - np.max(self.x)
        output = np.exp(x_wo_of) / np.sum(np.exp(x_wo_of))
        self.batch_size = x.shape[1]
        loss = (np.sum(-1 * self.t * np.log(output + self.epsilone))) / self.batch_size
        return loss
    
    def backward(self):
        output = (self.x - self.t)/self.batch_size
        return output