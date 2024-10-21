import numpy as np
from .loss import Softmax_CE_loss
from .utils import ReLU, im2col, col2im

class Linear():
    def __init__(self, learning_rate, in_num, out_num):
        self.learning_rate = learning_rate
        self.weight = 1/np.sqrt(in_num)*np.random.randn(in_num,out_num)
        self.bias = 1/np.sqrt(in_num)*np.random.randn(out_num)
        self.x = None
        
    def forward(self, x):
        self.x = x
        return np.dot(x,self.weight)+self.bias
    
    def backward(self, output_gradient):
        input_gradient = np.dot(output_gradient, np.transpose(self.weight))
        weight_gradient = np.dot(np.transpose(self.x), output_gradient)
        
        self.weight = self.weight - self.learning_rate*weight_gradient
        self.bias = self.bias - np.sum(output_gradient,axis =0)*self.learning_rate
        
        return input_gradient
    

class NN():
    def __init__(self, learning_rate):
        self.inputs = [0]*6
        self.learning_rate = learning_rate
        self.input = None
        self.gt = None
        self.linear1 = Linear(self.learning_rate,784, 196)
        self.ReLU1 = ReLU()
        self.linear2 = Linear(self.learning_rate,196, 49)
        self.ReLU2 = ReLU()
        self.linear3 = Linear(self.learning_rate,49, 10)
        self.softmax_ce_loss = Softmax_CE_loss()
        
    def forward(self,x,y):
        self.input = x
        self.gt = y
        self.inputs[0] = self.linear1.forward(self.input)
        self.inputs[1] = self.ReLU1.forward(self.inputs[0])
        self.inputs[2] = self.linear2.forward(self.inputs[1])
        self.inputs[3] = self.ReLU2.forward(self.inputs[2])
        self.inputs[4] = self.linear3.forward(self.inputs[3])
        return self.inputs[4]

    def backward(self):
        output_gradient = self.softmax_ce_loss.backward()
        output_gradient = self.linear3.backward(output_gradient)
        output_gradient = self.ReLU2.backward(output_gradient)
        output_gradient = self.linear2.backward(output_gradient)
        output_gradient = self.ReLU1.backward(output_gradient)
        output_gradient = self.linear1.backward(output_gradient)
        return output_gradient
    
    def train(self,x,y):
        output = self.softmax_ce_loss.forward(self.forward(x,y),self.gt)
    
    def test(self,x,y):
        return np.sum(np.argmax(y, axis = -1)==np.argmax(self.forward(x,y), axis = -1))
        
    def confuse(self,x,y):
        return np.argmax(self.forward(x,y),axis=-1),np.argmax(y,axis=-1)
    
    def top3(self,x,y):
        out = self.softmax_ce_loss.prob(self.forward(x,y))
        return np.argmax(out), np.max(out)
        
    def loss(self,x,y):
        output = self.softmax_ce_loss.forward(self.forward(x,y),self.gt)
        return output


class MaxPooling():
    def __init__(self,kernel_size, stride = 1, padding = 0, batch_size = 100):
        self.x = None
        self.batch_size = batch_size
        self.kernel_size = kernel_size
        self.stride = stride
        self.padding = padding
        self.in_channels = None
        self.out_shape = None
        self.argmax_result = None
        self.t = None
        
    def forward(self,x):
        self.x = x
        N, C, H, W = x.shape
        self.out_shape = int(1+(self.x.shape[-1]-self.kernel_size+2*self.padding)/self.stride)
        
        col = im2col(self.x,self.kernel_size, self.kernel_size, self.stride,self.padding).reshape(-1,self.kernel_size**2)
        
        argmax_result = np.argmax(col, axis = 1)
        
        max_result = np.max(col, axis=1)
        max_result = max_result.reshape(N, self.out_shape, self.out_shape, C).transpose(0,3,1,2)
        
        self.argmax_result = argmax_result.flatten()
        
        return max_result
    
    def backward(self, output_gradient):
        output_gradient = output_gradient.transpose(0,2,3,1) 
        
        zero = np.zeros((output_gradient.size, self.kernel_size**2))
        zero[np.arange(self.argmax_result.size), self.argmax_result.flatten()] = output_gradient.flatten()
        
        zero = zero.reshape(output_gradient.shape +(self.kernel_size**2,))
        zero = zero.reshape(zero.shape[0]*zero.shape[1]*zero.shape[2],-1)
        
        img = col2im(zero,self.x.shape,self.kernel_size, self.kernel_size, self.stride, self.padding)
        
        return img


class Linear_for_conv():
    def __init__(self, learning_rate, in_num, out_num):
        self.learning_rate = learning_rate
        self.weight = 1/np.sqrt(in_num)*np.random.randn(in_num,out_num)
        self.bias = 1/np.sqrt(in_num)*np.random.randn(out_num)
        self.x = None
        self.x_size = None
        
    def forward(self, x):
        self.x_shape = x.shape
        self.x = x.reshape(x.shape[0],-1)
        return np.dot(self.x,self.weight)+self.bias
    
    def backward(self, output_gradient):
        input_gradient = np.dot(output_gradient, np.transpose(self.weight)).reshape(self.x_shape) # 한번더 확인
        weight_gradient = np.dot(np.transpose(self.x), output_gradient)
        
        self.weight = self.weight - self.learning_rate*weight_gradient
        
        return input_gradient


class convolution():
    def __init__(self, learning_rate, in_channels, size, out_channels, kernel_size, batch_size = 100, stride = 1, padding = 0):
        self.learning_rate = learning_rate
        self.kernel_size = kernel_size
        self.in_channels = in_channels
        self.out_channels = out_channels
        self.batch_size = batch_size
        self.width = size
        self.height = size
        self.stride = stride
        self.padding = padding
        self.t = None
        self.x = None
        self.col = None
        self.out_shape = None
        self.weight = (np.sqrt(2/(self.in_channels*self.width*self.height + self.out_channels*self.width*self.height))*np.random.randn(self.out_channels,self.in_channels,self.kernel_size,self.kernel_size))
        self.bias = (np.sqrt(2/(self.in_channels*self.width*self.height + self.out_channels*self.width*self.height))*np.random.randn(self.batch_size, self.out_channels,self.width,self.height)).reshape(self.width*self.height*self.batch_size,self.out_channels)
        
    def forward(self, x):
        self.x = x
        FN, C, FH, FW = self.weight.shape
        N, C, H, W = x.shape
        self.out_shape = int(1+(self.x.shape[-1]-self.kernel_size+2*self.padding)/self.stride)
        col = im2col(self.x, FH, FW, self.stride, self.padding)
        col_W = self.weight.reshape(FN,-1).T
        
        self.col = col
        self.col_W = col_W
        dot_result = np.dot(col,col_W)+self.bias
        dot_result = dot_result.reshape(N, self.out_shape, self.out_shape, -1).transpose(0,3,1,2)
        
        return dot_result
    
    def backward(self, output_gradient):
        FN, C, FH, FW = self.weight.shape
        self.output_gradient = output_gradient.transpose(0,2,3,1).reshape(-1,FN)
        
        self.db = np.sum(self.output_gradient,axis = 0)
        weight_gradient = np.dot(self.col.T,self.output_gradient)
        weight_gradient = weight_gradient.transpose(1,0).reshape(FN,C,FH, FW)
        
        out = np.dot(self.output_gradient, self.col_W.T)
        
        out = col2im(out, self.x.shape, FH, FW, self.stride, self.padding)
        
        self.weight -= self.learning_rate*weight_gradient
        
        return out
    

class CNN():
    def __init__(self, learning_rate, batch_size):
        self.inputs = [0]*7
        self.learning_rate = learning_rate
        self.input = None
        self.gt = None
        self.maxPool1 = MaxPooling(kernel_size=2, stride=2, padding = 0, batch_size=batch_size)
        self.maxPool2 = MaxPooling(kernel_size=2, stride=2, padding = 0, batch_size=batch_size)
        self.conv1 = convolution(self.learning_rate, in_channels = 1, size = 28, out_channels = 2, kernel_size = 3, stride = 1, padding = 1, batch_size = batch_size)
        self.ReLU1 = ReLU()
        self.conv2 = convolution(self.learning_rate, in_channels = 2, size = 14, out_channels = 4, kernel_size = 3, stride = 1, padding = 1, batch_size = batch_size)
        self.ReLU2 = ReLU()
        self.linear = Linear_for_conv(self.learning_rate,49*4, 10)
        self.softmax_ce_loss = Softmax_CE_loss()
        
    def forward(self,x,y):
        self.input = x
        self.gt = y
        self.inputs[0] = self.conv1.forward(self.input)
        self.inputs[1] = self.ReLU1.forward(self.inputs[0])
        self.inputs[2] = self.maxPool1.forward(self.inputs[1])
        self.inputs[3] = self.conv2.forward(self.inputs[2])
        self.inputs[4] = self.ReLU2.forward(self.inputs[3])
        self.inputs[5] = self.maxPool2.forward(self.inputs[4])
        self.inputs[6] = self.linear.forward(self.inputs[5])
        return self.inputs[6]
        
    def backward(self):
        output_gradient = self.softmax_ce_loss.backward()
        output_gradient = self.linear.backward(output_gradient)
        output_gradient = self.maxPool2.backward(output_gradient)
        output_gradient = self.ReLU2.backward(output_gradient)
        output_gradient = self.conv2.backward(output_gradient)
        output_gradient = self.maxPool1.backward(output_gradient)
        output_gradient = self.ReLU1.backward(output_gradient)
        output_gradient = self.conv1.backward(output_gradient)
        return output_gradient
    
    def train(self,x,y):
        output = self.softmax_ce_loss.forward(self.forward(x,y),self.gt)
        return output
    
    def test(self,x,y):
        return np.sum(np.argmax(y, axis = -1)==np.argmax(self.forward(x,y), axis = -1))
    
    def confuse(self,x,y):
        return np.argmax(self.forward(x,y),axis=-1),np.argmax(y,axis=-1)
    
    def top3(self,x,y):
        out = self.softmax_ce_loss.prob(self.forward(x,y))
        return np.argmax(out, axis=-1), np.max(out, axis = -1)
        
    def loss(self,x,y):
        output = self.softmax_ce_loss.forward(self.forward(x,y),self.gt)
        return output