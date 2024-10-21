from .utils import norm


def NN_train(NN, train_dataset, batch_size):
    train_loss = []
    for i, train_data in enumerate(train_dataset):
        if i+1 == train_dataset.__len__():
            train_loss.append(NN.loss(norm(train_data[:][0].reshape(batch_size,784)),norm(train_data[:][1])))
        NN.train(norm(train_data[:][0].reshape(batch_size,784)),norm(train_data[:][1]))
        NN.backward()
    return train_loss
        
def NN_test(NN, test_dataset, batch_size):
    test_loss = []
    correct = 0
    for i, test_data in enumerate(test_dataset):
        if i+1 == test_dataset.__len__():
            test_loss.append(NN.loss(norm(test_data[:][0].reshape(batch_size,784)),norm(test_data[:][1])))
        correct += NN.test(norm(test_data[:][0].reshape(batch_size,784)),norm(test_data[:][1]))
    test_accuracy = correct / (test_dataset.__len__()*batch_size) * 100
    return test_loss, test_accuracy

def CNN_train(CNN, train_dataset, batch_size):
    train_loss = []
    for i, train_data in enumerate(train_dataset):
        if i+1 == train_dataset.__len__():
            train_loss.append(CNN.loss(norm(train_data[:][0].reshape(batch_size,1,28,28)),norm(train_data[:][1])))
        CNN.train(norm(train_data[:][0].reshape(batch_size,1,28,28)),norm(train_data[:][1]))
        CNN.backward()
    return train_loss
        
def CNN_test(CNN, test_dataset, batch_size):
    test_loss = []
    correct = 0
    for i, test_data in enumerate(test_dataset):
        if i+1 == test_dataset.__len__():
            test_loss.append(CNN.loss(norm(test_data[:][0].reshape(batch_size,1,28,28)),norm(test_data[:][1])))
        correct += CNN.test(norm(test_data[:][0].reshape(batch_size,1,28,28)),norm(test_data[:][1]))
    test_accuracy = correct / (test_dataset.__len__()*batch_size) * 100
    return test_loss, test_accuracy