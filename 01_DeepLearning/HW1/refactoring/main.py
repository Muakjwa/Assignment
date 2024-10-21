from dataset import dataloader
import src.module as module
import src.trainer as trainer
import src.utils as utils

batch_size = 100
epsilone = 0.000001
NN_learning_rate = 0.001
CNN_learning_rate = 0.01
epochs = 100

NN_train_loss, NN_test_loss = [], []
CNN_train_loss, CNN_test_loss = [], []

train_dataset = dataloader.Dataloader("dataset", is_train = True, shuffle = True, batch_size = batch_size)
test_dataset = dataloader.Dataloader("dataset", is_train = False, shuffle = True, batch_size = batch_size)

NN = module.NN(NN_learning_rate)

for i in range(epochs):
    train_loss = trainer.NN_train(NN, train_dataset, batch_size)
    test_loss, NN_test_accuracy = trainer.NN_test(NN, test_dataset, batch_size)
    NN_train_loss.append(train_loss); NN_test_loss.append(test_loss)
    if (i % 10 == 9):
        print(i+1,'Epoch Finished', end = '\t')
        print(f"Accuracy : {round(NN_test_accuracy, 2)}%")

utils.plot_epoch_loss(NN_train_loss, NN_test_loss, epochs)
utils.plot_NN_confusion_matrix(NN, test_dataset, batch_size)
utils.plot_NN_top3(NN, test_dataset, batch_size)

CNN = module.CNN(CNN_learning_rate, batch_size)

for i in range(epochs):
    train_loss = trainer.CNN_train(CNN, test_dataset, batch_size)
    test_loss, CNN_test_accuracy = trainer.CNN_test(CNN, test_dataset, batch_size)
    CNN_train_loss.append(train_loss); CNN_test_loss.append(test_loss)    
    if (i % 10 == 9):
        print(i+1,'Epoch Finished', end = '\t')
        print(f"Accuracy : {round(CNN_test_accuracy, 2)}%")

utils.plot_epoch_loss(CNN_train_loss, CNN_test_loss, epochs)
utils.plot_CNN_confusion_matrix(CNN, test_dataset, batch_size)
utils.plot_CNN_top3(CNN, test_dataset, batch_size)