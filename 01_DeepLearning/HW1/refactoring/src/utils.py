import numpy as np
import matplotlib.pyplot as plt
import matplotlib.cm as cm
import seaborn as sns

# min-max normalization
def norm(x):
    return (x-np.min(x))/(np.max(x) - np.min(x))

class ReLU():
    def __init__(self):
        self.x = None
    
    def length(self,x):
        return len(x)
    
    def forward(self,x):
        self.x = x
        return np.maximum(0,x)
    
    def backward(self,output_gradient):
        return (self.x>0)*output_gradient

"""
For CNN processing
"""
def im2col(input_data, filter_h, filter_w, stride=1, pad=0):
    N, C, H, W = input_data.shape
    out_h = (H + 2*pad - filter_h)//stride + 1
    out_w = (W + 2*pad - filter_w)//stride + 1

    img = np.pad(input_data, [(0,0), (0,0), (pad, pad), (pad, pad)], 'constant')
    col = np.zeros((N, C, filter_h, filter_w, out_h, out_w))

    for y in range(filter_h):
        y_max = y + stride*out_h
        for x in range(filter_w):
            x_max = x + stride*out_w
            col[:, :, y, x, :, :] = img[:, :, y:y_max:stride, x:x_max:stride]

    col = col.transpose(0, 4, 5, 1, 2, 3).reshape(N*out_h*out_w, -1)
    return col

def col2im(col, input_shape, filter_h, filter_w, stride=1, pad=0):    
    N, C, H, W = input_shape
    out_h = (H + 2*pad - filter_h) // stride + 1
    out_w = (W + 2*pad - filter_w) // stride + 1
    col = col.reshape(N, out_h, out_w, C, filter_h, filter_w).transpose(0, 3, 4, 5, 1, 2)
    
    img = np.zeros((N, C, H + 2*pad + stride - 1, W + 2*pad + stride - 1))
    for y in range(filter_h):
        y_max = y + stride*out_h
        for x in range(filter_w):
            x_max = x + stride*out_w
            img[:, :, y:y_max:stride, x:x_max:stride] += col[:, :, y, x, :, :]
            
    return img[:, :, pad:H + pad, pad:W + pad]


"""
Graph
: Plotting Graph
"""
def plot_epoch_loss(train_loss, test_loss, epochs):
    x = np.arange(1, epochs+1)
    plt.plot(x, train_loss, 'r', label="train")
    plt.plot(x, test_loss, 'b', label = "test")
    plt.title("Loss")
    plt.legend(loc = 'upper right')
    plt.show()

def plot_NN_confusion_matrix(model, test_dataset, batch_size):
    confuse_matrix = np.zeros((10,10))
    target_num = [0]*10
    length = test_dataset.__len__()
    for i in range(length):
        for j in range(batch_size):
            c_train, c_test = model.confuse(test_dataset.__getitem__(i)[0][j].reshape(1,784),test_dataset.__getitem__(i)[1][j])
            confuse_matrix[c_train,c_test] += 1
            target_num[c_test] +=1
            
    for i in range(10):
        confuse_matrix[:,i] = np.round(np.divide(confuse_matrix[:,i],target_num[i]),2)
        
    sns.heatmap(confuse_matrix, cmap = "Blues", annot = True)
    plt.title("Confusion Matrix")
    plt.ylabel("Prediction")
    plt.xlabel("Target")
    plt.show()

def plot_CNN_confusion_matrix(model, test_dataset, batch_size):
    confuse_matrix = np.zeros((10,10))
    target_num = [0]*10
    length = test_dataset.__len__()
    for i, test_data in enumerate(test_dataset):
        c_train, c_test = model.confuse(norm(test_data[:][0].reshape(batch_size,1,28,28)),norm(test_data[:][1]))
        for j in range(len(c_train)):
            confuse_matrix[c_train[j],c_test[j]] += 1
            target_num[c_test[j]] +=1
            
    for i in range(10):
        confuse_matrix[:,i] = np.round(np.divide(confuse_matrix[:,i],target_num[i]),2)
        
    sns.heatmap(confuse_matrix, cmap = "Blues", annot = True)
    plt.title("Confusion Matrix")
    plt.ylabel("Prediction")
    plt.xlabel("Target")
    plt.show()

def plot_NN_top3(model, test_dataset, batch_size):
    target_num = [0]*10
    pred_num = []
    for i in range(10):
        pred_num.append([0])
        pred_num[i].remove(0)
    length = test_dataset.__len__()
    for i in range(length):
        for j in range(batch_size):
            idx, val = model.top3(test_dataset.__getitem__(i)[0][j].reshape(1,784), test_dataset.__getitem__(i)[1][j])
            pred_num[idx].append([val,i,j])
            
    for i in range(len(target_num)):
        pred_num[i].sort(reverse = True)

    plt.figure(figsize = (3,10))
    for i in range(10):
        for j in range(3):
            plt.subplot(10,3,i*3+j+1)
            plt.imshow(test_dataset.__getitem__(pred_num[i][j][1])[0][pred_num[i][j][2]].reshape(28,28), cmap=cm.binary)
            plt.gca().axes.xaxis.set_visible(False)
            plt.gca().axes.yaxis.set_visible(False)
    
    for i in range(10):
        print(i,": ",end='')
        for j in range(3):
            print(f"{round(100*pred_num[i][j][0],2)}%",end="    ")
        print()

def plot_CNN_top3(model, test_dataset, batch_size):
    target_num = [0]*10
    pred_num = []
    for i in range(10):
        pred_num.append([0])
        pred_num[i].remove(0)
    length = test_dataset.__len__()
    for i, test_data in enumerate(test_dataset):
        idx, val = model.top3(norm(test_data[:][0].reshape(batch_size,1,28,28)),norm(test_data[:][1]))
        for j in range(test_dataset.__len__()):
            pred_num[idx[j]].append([val[j],i,j])
            
    for i in range(len(target_num)):
        pred_num[i].sort(reverse = True)

    plt.figure(figsize = (3,10))
    for i in range(10):
        for j in range(3):
            plt.subplot(10,3,i*3+j+1)
            plt.imshow(test_dataset.__getitem__(pred_num[i][j][1])[0][pred_num[i][j][2]].reshape(28,28), cmap=cm.binary)
            plt.gca().axes.xaxis.set_visible(False)
            plt.gca().axes.yaxis.set_visible(False)
    
    for i in range(10):
        print(i,": ",end='')
        for j in range(3):
            print(f"{round(100*pred_num[i][j][0],2)}%",end="    ")
        print()