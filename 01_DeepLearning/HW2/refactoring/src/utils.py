import numpy as np
import matplotlib.pyplot as plt
from data_train_test import emo_utils

def plot_epoch_loss(train_loss, test_loss, accuracy, epochs = 500):
    x = np.arange(epochs)
    plt.figure(figsize = (12,5))
    plt.subplot(1,2,1)
    plt.plot(x, train_loss, label = 'train_loss')
    plt.plot(x, test_loss, label = 'test_loss')
    plt.gca().set_title("RNN + 50d + SGD Loss")
    plt.legend()
    plt.subplot(1,2,2)
    plt.plot(x, accuracy, label = 'accuracy')
    plt.legend()
    plt.gca().set_title("RNN + 50d + SGD Accuracy")

def print_prediction_label(model, test_for_vec, test_label):
    pred_emoji = []
    target_emoji = []
    for i in range(56):
        out = model.forward(test_for_vec[i], test_label[i][:,np.newaxis])
        pred_emoji.append(np.argmax(out))
        target_emoji.append(np.argmax(test_label[i]))
    print("target : \t")
    for i in range(len(target_emoji)):
        print(emo_utils.label_to_emoji(target_emoji[i]),end = '')
        print(emo_utils.label_to_emoji(pred_emoji[i]), end = '')
        if target_emoji[i] == pred_emoji[i]:
            print("True")
        else:
            print("False")