from data_train_test import emo_utils
from src import module
from src import trainer
from src import utils
import numpy as np

epsilone = 0.000001

d50 =emo_utils.read_glove_vecs('glove.6B/glove.6B.50d.txt')
d100 = emo_utils.read_glove_vecs('glove.6B/glove.6B.100d.txt')

all_emoji = emo_utils.read_csv('data_train_test/emojify_data.csv')
train_emoji = emo_utils.read_csv('data_train_test/train_emoji.csv')
test_emoji = emo_utils.read_csv('data_train_test/test_emoji.csv')

train_for_vec = []
for i in range(len(train_emoji[0])):
    words = train_emoji[0][i].split()
    train_for_vec.append(words)
    
test_for_vec = []
for i in range(len(test_emoji[0])):
    words = test_emoji[0][i].split()
    test_for_vec.append(words)

train_label = np.array([[0]*5 for _ in range(132)])
for i in range(132):
    train_label[i,train_emoji[1][i]]=1
    
test_label = np.array([[0]*5 for _ in range(132)])
for i in range(56):
    test_label[i,test_emoji[1][i]]=1

epohcs = 500
batch_size = 1
Rnn = module.RNN(0.0005, batch_size, 50, d50)
RNN_train_loss, RNN_test_loss, RNN_accuracy = trainer.train_model(Rnn, train_for_vec, test_for_vec, train_label, test_label, epohcs, batch_size)

utils.plot_epoch_loss(RNN_train_loss, RNN_test_loss, RNN_accuracy, epohcs)
utils.print_prediction_label(Rnn, test_for_vec, test_label)

lstm_50 = module.LSTM(0.01, batch_size, 50, d50)
LSTM_train_loss, LSTM_test_loss, LSTM_accuracy = trainer.train_model(lstm_50, train_for_vec, test_for_vec, train_label, test_label, epohcs, batch_size)

utils.plot_epoch_loss(LSTM_train_loss, LSTM_test_loss, LSTM_accuracy, epohcs)
utils.print_prediction_label(lstm_50, test_for_vec, test_label)

lstm_50_adam = module.LSTM(0.01, batch_size, 50, d50)
LSTM_train_loss, LSTM_test_loss, LSTM_accuracy = trainer.train_model(lstm_50_adam, train_for_vec, test_for_vec, train_label, test_label, epohcs, batch_size, 'Adam')

utils.plot_epoch_loss(LSTM_train_loss, LSTM_test_loss, LSTM_accuracy, epohcs)
utils.print_prediction_label(lstm_50_adam, test_for_vec, test_label)

lstm_100 = module.LSTM(0.05, batch_size, 100, d100)
LSTM_train_loss, LSTM_test_loss, LSTM_accuracy = trainer.train_model(lstm_100, train_for_vec, test_for_vec, train_label, test_label, epohcs, batch_size)

utils.plot_epoch_loss(LSTM_train_loss, LSTM_test_loss, LSTM_accuracy, epohcs)
utils.print_prediction_label(lstm_100, test_for_vec, test_label)

lstm_50_dropout = module.LSTM(0.01, batch_size, 50, d50, 0.2)
LSTM_train_loss, LSTM_test_loss, LSTM_accuracy = trainer.train_model(lstm_50_dropout, train_for_vec, test_for_vec, train_label, test_label, epohcs, batch_size)

utils.plot_epoch_loss(LSTM_train_loss, LSTM_test_loss, LSTM_accuracy, epohcs)
utils.print_prediction_label(lstm_50_dropout, test_for_vec, test_label)