import numpy as np

def train_model(model, train_for_vec, test_for_vec, train_label, test_label, epochs = 500, batch_size = 1, optimizer = 'SGD'):
    correct = 0
    train_loss =[] 
    test_loss = []
    accuracy = []
    for j in range(epochs):
        for i in range(132 // batch_size):
            loss = model.loss(train_for_vec[i], train_label[i][:,np.newaxis])
            if (optimizer == 'Adam'):
                model.Adam()
            else:
                model.GD()
            if i==132 // batch_size - 1:
                train_loss.append(loss)
        for i in range(56 // batch_size):
            out = model.forward(test_for_vec[i], test_label[i][:,np.newaxis])
            if np.argmax(out) == np.argmax(test_label[i]):
                correct+=1
            if i == 56 // batch_size - 1:
                loss = model.loss(test_for_vec[i], test_label[i][:,np.newaxis])
                test_loss.append(loss)
        if ((j + 1) % 100 == 0):
            print(j+1,"번째 iter :",train_loss[j])
            print("Accuracy :",correct/56)
        accuracy.append(correct/56)
        correct = 0
    return train_loss, test_loss, accuracy