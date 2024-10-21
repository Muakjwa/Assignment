import numpy as np
from .loss import Softmax_CE_loss
from .activation import tanh, sigmoid

class RNN():
    def __init__(self, learning_rate, batch_size, Bow_len, vector):
        self.batch_size = batch_size
        self.learning_rate = learning_rate
        self.Bow_len = Bow_len
        self.vector = vector
        self.prev_h_t = np.random.randn(5, self.batch_size)*np.sqrt(1/25)
        # parameters 초기화
        self.W_hh = np.random.randn(5, 5)*np.sqrt(1/25)
        self.W_xh = np.random.randn(5, self.Bow_len)*np.sqrt(1/25)
        self.b_h = np.random.randn(5, 1)*np.sqrt(1/25)
        self.W_hy = np.random.randn(5, 5)*np.sqrt(1/25)
        self.b_y = np.random.randn(5, 1)*np.sqrt(1/25)
        # tanh, softmax 정의
        self.tanh = tanh()
        self.softmax = Softmax_CE_loss()
        self.information = None
        self.y_t = None
        
        self.first_moment = [0]*5
        self.second_moment = [0]*5
        self.first_unbias = [0]*5
        self.second_unbias = [0]*5
        self.count = 1
        
    def forward(self, x, y):
        self.information = []
        for i in range(len(x)):
            h_t = self.tanh.forward(self.W_hh.dot(self.prev_h_t) + self.W_xh.dot(self.vector[2][x[i].lower()][:,np.newaxis]) + self.b_h)
            # backpropagation에서 사용할 정보 저장 (매 layer의 x_t, h_t-1, h_t)
            self.information.append((self.vector[2][x[i].lower()][:,np.newaxis], self.prev_h_t, h_t))
            self.prev_h_t = h_t
        out = np.dot(self.W_hy, h_t) + self.b_y
        return out
        
    def backward(self):
        output_gradient = self.softmax.backward()
        dW_hh, dW_xh, dW_hy, db_h, db_y = np.zeros((5,5)), np.zeros((5,self.Bow_len)), np.zeros((5,5)), np.zeros((5,1)), np.zeros((5,1))
        # y_t = softmax( W_hy * h_t + b_y ) 의 backpropagation
        
        dW_hy += np.dot(output_gradient, self.information[-1][2].T)
        db_y += np.sum(output_gradient, keepdims = True, axis = -1)
        output_gradient = np.dot(self.W_hy.T, output_gradient)
            
        for i in range(len(self.information)-1, -1, -1):
            # h_t = tanh( W_hh * h_t-1 + W_hx * x_t + b_h ) 의 backpropagation
            # h_t와 output gradient를 받아와 tanh의 backward 진행      ( 1 - h_t**2 ) * output_gradient가 되어야한다.
            
            #output_gradient = self.tanh.backward(self.information[i][2]) * output_gradient
            output_gradient = (1 - self.information[i][2]**2) * output_gradient
            #output_gradient = self.tanh.backward(output_gradient)
            db_h += np.sum(output_gradient, keepdims = True, axis = -1)
            dW_hh += np.dot(output_gradient, self.information[i][1].T)
            dW_xh += np.dot(output_gradient, self.information[i][0].T)
            output_gradient = np.dot(self.W_hh.T, output_gradient)
            
        # dW_hh, dW_xh, dW_hy, db_h, db_y 순서로 tuple로 return (SGD나 ADAM으로 이어짐)
        return [dW_hh, dW_xh, dW_hy, db_h, db_y]
    
    def loss(self, x, y):
        out = self.forward(x,y)
        self.y_t = self.softmax.forward(out,y)
        return self.y_t
    
    def GD(self):
        # GD 함수를 사용하면 backward를 한 결과 gradient를 빼준다.
        gradient = self.backward()
        self.W_hh -= (self.learning_rate * gradient[0] / self.batch_size)
        self.W_xh -= (self.learning_rate * gradient[1] / self.batch_size)
        self.W_hy -= (self.learning_rate * gradient[2] / self.batch_size)
        self.b_h -= (self.learning_rate * gradient[3] / self.batch_size)
        self.b_y -= (self.learning_rate * gradient[4] / self.batch_size)
        
    def SGD(self,x,y):
        vec = np.zeros((10, self.batch_size, len(self.vector[2]['his'])))
        for i in range(self.batch_size):
            for j in range(len(x[i])):
                vec[j,i] = self.vector[2][x[i][j].lower()]
        self.information = []
        for i in range(self.batch_size):
            h_t = self.tanh.forward(self.W_hh.dot(self.prev_h_t) + self.W_xh.dot(vec[i].T) + self.b_h)
            # backpropagation에서 사용할 정보 저장 (매 layer의 x_t, h_t-1, h_t)
            self.information.append((vec[i].T, self.prev_h_t, h_t))
            self.prev_h_t = h_t
        out = np.dot(self.W_hy, h_t) + self.b_y
        self.y_t = self.softmax.forward(out,y.T)
        self.GD()
        return self.y_t
    
    def SGD_forward_only(self,x,y):
        vec = np.zeros((10, self.batch_size, len(self.vector[2]['his'])))
        for i in range(self.batch_size):
            for j in range(len(x[i])):
                vec[j,i] = self.vector[2][x[i][j].lower()]
        self.information = []
        for i in range(self.batch_size):
            h_t = self.tanh.forward(self.W_hh.dot(self.prev_h_t) + self.W_xh.dot(vec[i].T) + self.b_h)
            # backpropagation에서 사용할 정보 저장 (매 layer의 x_t, h_t-1, h_t)
            self.information.append((vec[i].T, self.prev_h_t, h_t))
            self.prev_h_t = h_t
        out = np.dot(self.W_hy, h_t) + self.b_y
        return out
        
    def Adam(self, beta1 = 0.9, beta2 = 0.999):
        gradient = self.backward()
        for _ in range(1000):
            for i in range(len(gradient)):
                self.first_moment[i] = beta1 * self.first_moment[i] + (1-beta1)*gradient[i]
                self.second_moment[i] = beta2 * self.second_moment[i] + (1-beta2)*gradient[i]*gradient[i]
                self.first_unbias[i] = self.first_moment[i] / (1-beta1**self.count)
                self.second_unbias[i] = self.second_moment[i] / (1-beta2**self.count)
            self.W_hh -= (self.learning_rate * self.first_unbias[0]/(np.sqrt(self.second_unbias[0]+1e07)))
            self.W_xh -= (self.learning_rate * self.first_unbias[1]/(np.sqrt(self.second_unbias[1]+1e07)))
            self.W_hy -= (self.learning_rate * self.first_unbias[2]/(np.sqrt(self.second_unbias[2]+1e07)))
            self.b_h -= (self.learning_rate * self.first_unbias[3]/(np.sqrt(self.second_unbias[3]+1e07)))
            self.b_y -= (self.learning_rate * self.first_unbias[4]/(np.sqrt(self.second_unbias[4]+1e07)))
            self.count+=1


class LSTM():
    def __init__(self, learning_rate, batch_size, Bow_len, vector, Drop = 0):
        self.batch_size = batch_size
        self.learning_rate = learning_rate
        self.Bow_len = Bow_len
        self.Drop = Drop
        self.d50 = vector
        self.vector = vector
        self.prev_a_t1, self.prev_a_t2, self.prev_c_t1, self.prev_c_t2 = np.random.randn(5, self.batch_size)*np.sqrt(1/5), np.random.randn(5, self.batch_size)*np.sqrt(1/5),np.random.randn(5, self.batch_size)*np.sqrt(1/5), np.random.randn(5, self.batch_size)*np.sqrt(1/5)
        # parameters 초기화
        self.W_y = np.random.randn(5, 5)*np.sqrt(1/5)
        self.b_y = np.random.randn(5, 1)*np.sqrt(1/5)
        
        self.W_1 = np.random.randn(20, Bow_len + 5)*np.sqrt(1/20)
        self.b_1 = np.random.randn(20, 1)*np.sqrt(1/20)
        self.W_2 = np.random.randn(20, 5 + 5)*np.sqrt(1/20)
        self.b_2 = np.random.randn(20, 1)*np.sqrt(1/20)
        
        # tanh, softmax 정의
        self.tanh = tanh()
        self.softmax = Softmax_CE_loss()
        self.sigmoid = sigmoid()
        self.information = None
        self.y_t = None
        
        # Adam parameter
        self.first_moment = [0]*6
        self.second_moment = [0]*6
        self.first_unbias = [0]*6
        self.second_unbias = [0]*6
        self.count = 1
        
        
    def forward(self, x, y):
        self.information = []
        for i in range(len(x)):
            concat_prev_a_t1_x = np.concatenate((self.prev_a_t1, self.d50[2][x[i].lower()][:,np.newaxis]), axis = 0)
            
            out = np.dot(self.W_1, concat_prev_a_t1_x) + self.b_1
            
            f_t1 = self.sigmoid.forward(out[:5, :])
            cc_t1 = self.tanh.forward(out[5:10, :])
            i_t1 = self.sigmoid.forward(out[10:15, :])
            o_t1 = self.sigmoid.forward(out[15:, :])
            
            c_t1 = f_t1*self.prev_c_t1 + i_t1*cc_t1
            a_t1 = o_t1*self.tanh.forward(c_t1)
            
            P_drop = np.random.choice([0, 1], p=[1 - self.Drop, self.Drop])
            
            # Dropout 의 경우 때문에 a_t1을 self.Drop으로 나눠줌
            if self.Drop != 0:
                a_t1 /= (1-self.Drop)
            
            if P_drop == 0:
                concat_prev_a_t2_a_t1 = np.concatenate((self.prev_a_t2, a_t1), axis = 0)
            else:
                concat_prev_a_t2_a_t1 = np.concatenate((self.prev_a_t2, np.zeros_like(a_t1)), axis = 0)
            
            #if self.Drop != 0:
            #    concat_prev_a_t2_a_t1/=self.Drop
            
            out2 = np.dot(self.W_2, concat_prev_a_t2_a_t1) + self.b_2
            
            f_t2 = self.sigmoid.forward(out2[:5, :])
            cc_t2 = self.tanh.forward(out2[5:10, :])
            i_t2 = self.sigmoid.forward(out2[10:15, :])
            o_t2 = self.sigmoid.forward(out2[15:, :])
            
            c_t2 = f_t2*self.prev_c_t2 + i_t2*cc_t2
            a_t2 = o_t2*self.tanh.forward(c_t2)
            
            # backpropagation에서 사용할 정보 저장 (매 layer의 Drop 여부, x_t, prev_a_t1, a_t1, prev_a_t2, a_t2, prev_c_t1, c_t1, prev_c_t2, c_t2, o_t1, o_t2, i_t1, i_t2, cc_t1, cc_t2, f_t1, f_t2)
            self.information.append((P_drop, self.d50[2][x[i].lower()][:,np.newaxis], self.prev_a_t1, a_t1, self.prev_a_t2, a_t2, self.prev_c_t1, c_t1, self.prev_c_t2, c_t2, o_t1, o_t2, i_t1, i_t2, cc_t1, cc_t2, f_t1, f_t2))
            self.prev_a_t1, self.prev_a_t2, self.prev_c_t1, self.prev_c_t2 = a_t1, a_t2, c_t1, c_t2
            
        out = np.dot(self.W_y, a_t2) + self.b_y
        return out
    
    def forward_dropout_test(self, x, y):
        self.information = []
        for i in range(len(x)):
            concat_prev_a_t1_x = np.concatenate((self.prev_a_t1, self.d50[2][x[i].lower()][:,np.newaxis]), axis = 0)
            
            out = np.dot(self.W_1, concat_prev_a_t1_x) + self.b_1
            
            f_t1 = self.sigmoid.forward(out[:5, :])
            cc_t1 = self.tanh.forward(out[5:10, :])
            i_t1 = self.sigmoid.forward(out[10:15, :])
            o_t1 = self.sigmoid.forward(out[15:, :])
            
            c_t1 = f_t1*self.prev_c_t1 + i_t1*cc_t1
            a_t1 = o_t1*self.tanh.forward(c_t1)
            
            concat_prev_a_t2_a_t1 = np.concatenate((self.prev_a_t2, a_t1), axis = 0)
            
            out2 = np.dot(self.W_2, concat_prev_a_t2_a_t1) + self.b_2
            
            f_t2 = self.sigmoid.forward(out2[:5, :])
            cc_t2 = self.tanh.forward(out2[5:10, :])
            i_t2 = self.sigmoid.forward(out2[10:15, :])
            o_t2 = self.sigmoid.forward(out2[15:, :])
            
            c_t2 = f_t2*self.prev_c_t2 + i_t2*cc_t2
            a_t2 = o_t2*self.tanh.forward(c_t2)
            
        out = np.dot(self.W_y, a_t2) + self.b_y
        return out
    
    def loss(self, x, y):
        out = self.forward(x,y)
        self.y_t = self.softmax.forward(out, y)
        return self.y_t
    
    def loss_dropout_test(self, x, y):
        out = self.forward_dropout_test(x,y)
        self.y_t = self.softmax.forward(out, y)
        return self.y_t
            
    def backward(self):
        output_gradient = self.softmax.backward()
        dW_f1, dW_f2, dW_cc1, dW_cc2, dW_i1, dW_i2, dW_o1, dW_o2, db_f1, db_f2, db_cc1, db_cc2, db_i1, db_i2, db_o1, db_o2, dW_y, db_y \
        = np.zeros((5, self.Bow_len+5)), np.zeros((5, 5+5)), np.zeros((5, self.Bow_len+5)), np.zeros((5, 5+5)), np.zeros((5, self.Bow_len+5)), np.zeros((5, 5+5)), np.zeros((5, self.Bow_len+5)), np.zeros((5, 5+5)) \
        , np.zeros((5,1)), np.zeros((5,1)), np.zeros((5,1)), np.zeros((5,1)), np.zeros((5,1)), np.zeros((5,1)), np.zeros((5,1)), np.zeros((5,1)), np.zeros((5,5)), np.zeros((5,1))
        # y_t = softmax( W_y * a_t + b_y ) 의 backpropagation
        dW_y += np.dot(output_gradient, self.information[-1][5].T)
        db_y += np.sum(output_gradient, keepdims = True, axis = -1)
        
        output_gradient = np.dot(self.W_y.T, output_gradient)
        # o_t2 * da_t2 * (1 - tanh(c_t2)**2)
        dc_t2 = self.information[-1][11] * output_gradient * self.tanh.backward(self.information[-1][9]) 
        # dc_t1 의 update를 도와주기 위한 변수
        cnt = 0
        prev_da_t1 = np.zeros_like(self.prev_a_t1)
            
        for i in range(len(self.information)-1, -1, -1):
            # da_t2 * tanh(c_t2) * (o_t2 * (1 - o_t2))
            do_t2 = output_gradient * self.tanh.forward(self.information[i][9]) * self.sigmoid.backward(self.information[i][11])
            # (dc_t2 * i_t2) * (1 - tanh(cc_t2)**2)
            dcc_t2 = dc_t2 * self.information[i][13] * self.tanh.backward(self.information[i][15])
            # (dc_t2 * cc_t2) * (i_t2 * (1 - i_t2))
            di_t2 = dc_t2 * self.information[i][15] * self.sigmoid.backward(self.information[i][13])
            # (dc_t2 * prev_c_t2) * (f_t2 * (1 - f_t2))
            df_t2 = dc_t2 * self.information[i][8] * self.sigmoid.backward(self.information[i][17])

            concat_prev_a_t2_a_t1 = np.concatenate((self.information[i][4], self.information[i][3]), axis = 0)

            dW_f2 += np.dot(df_t2, concat_prev_a_t2_a_t1.T)
            dW_i2 += np.dot(di_t2, concat_prev_a_t2_a_t1.T)
            dW_o2 += np.dot(do_t2, concat_prev_a_t2_a_t1.T)
            dW_cc2 += np.dot(dcc_t2, concat_prev_a_t2_a_t1.T)

            db_f2 += np.sum(df_t2, keepdims = True, axis = -1)
            db_i2 += np.sum(di_t2, keepdims = True, axis = -1)
            db_o2 += np.sum(do_t2, keepdims = True, axis = -1)
            db_cc2 += np.sum(dcc_t2, keepdims = True, axis = -1)

            # gradient를 구한 이전 layer에서의 a의 gradient를 구하기 (prev_a_t2)
            output_gradient = (np.dot(self.W_2.T , np.vstack((df_t2,di_t2,do_t2,dcc_t2))))[:5 , :]
            # (prev_c_t2) 구하기
            dc_t2 = dc_t2 * self.information[i][17]
            # 1 layer의 a_t1의 gradient 구하기
            da_t1 = (np.dot(self.W_2.T , np.vstack((df_t2,di_t2,do_t2,dcc_t2))))[5: , :]
            
            '''
            # Dropout Backward
            if self.information[i][0] == 1:
                da_t1 = prev_da_t1
            else:
                da_t1 = da_t1 + prev_da_t1
            '''
            if cnt == 0 :
                # o_t1 * da_t1 * (1 - tanh(c_t1)**2)
                dc_t1 = self.information[-1][10] * da_t1 * self.tanh.backward(self.information[-1][7])
            else:
                dc_t1 = dc_t1 * self.information[i][16]
            cnt+=1

            # da_t1 * tanh(c_t1) * (o_t1 * (1 - o_t1))
            do_t1 = da_t1 * self.tanh.forward(self.information[i][7]) * self.sigmoid.backward(self.information[i][10])
            # (dc_t1 * i_t1) * (1 - tanh(cc_t1)**2)
            dcc_t1 = dc_t1 * self.information[i][12] * self.tanh.backward(self.information[i][14])
            # (dc_t1 * cc_t1) * (i_t1 * (1 - i_t1))
            di_t1 = dc_t1 * self.information[i][14] * self.sigmoid.backward(self.information[i][12])
            # (dc_t1 * prev_c_t1) * (f_t1 * (1 - f_t1))
            df_t1 = dc_t1 * self.information[i][6] * self.sigmoid.backward(self.information[i][16])

            concat_prev_a_t1_x = np.concatenate((self.information[i][2], self.information[i][1]), axis = 0)

            dW_f1 += np.dot(df_t1, concat_prev_a_t1_x.T)
            dW_i1 += np.dot(di_t1, concat_prev_a_t1_x.T)
            dW_o1 += np.dot(do_t1, concat_prev_a_t1_x.T)
            dW_cc1 += np.dot(dcc_t1, concat_prev_a_t1_x.T)

            db_f1 += np.sum(df_t1, keepdims = True, axis = -1)
            db_i1 += np.sum(di_t1, keepdims = True, axis = -1)
            db_o1 += np.sum(do_t1, keepdims = True, axis = -1)
            db_cc1 += np.sum(dcc_t1, keepdims = True, axis = -1)
            
            prev_da_t1 = (np.dot(self.W_1.T , np.vstack((df_t2,di_t2,do_t2,dcc_t2))))[5: , :]
            if np.shape(prev_da_t1)[0]!=5:
                prev_da_t1 = np.zeros_like(self.prev_a_t1)
        
        dW_1 = np.vstack((dW_f1, dW_cc1, dW_i1, dW_o1))
        db_1 = np.vstack((db_f1, db_cc1, db_i1, db_o1))
        dW_2 = np.vstack((dW_f2, dW_cc2, dW_i2, dW_o2))
        db_2 = np.vstack((db_f2, db_cc2, db_i2, db_o2))
        # dW_hh, dW_xh, dW_hy, db_h, db_y 순서로 tuple로 return (SGD나 ADAM으로 이어짐)
        return (dW_y, db_y, dW_1, dW_2, db_1, db_2)
        
    def GD(self):
        # GD 함수를 사용하면 backward를 한 결과 gradient를 빼준다.
        gradient = self.backward()
        self.W_y -= (self.learning_rate * gradient[0] / self.batch_size)
        self.b_y -= (self.learning_rate * gradient[1] / self.batch_size)
        self.W_1 -= (self.learning_rate * gradient[2] / self.batch_size)
        self.W_2 -= (self.learning_rate * gradient[3] / self.batch_size)
        self.b_1 -= (self.learning_rate * gradient[4] / self.batch_size)
        self.b_2 -= (self.learning_rate * gradient[5] / self.batch_size)
        
    def SGD(self,x,y):
        vec = np.zeros((10, self.batch_size, len(self.vector[2]['his'])))
        for i in range(self.batch_size):
            for j in range(len(x[i])):
                vec[j,i] = self.vector[2][x[i][j].lower()]
        self.information = []
        for i in range(len(x)):
            concat_prev_a_t1_x = np.concatenate((self.prev_a_t1, vec[i].T), axis = 0)
            
            out = np.dot(self.W_1, concat_prev_a_t1_x) + self.b_1
            
            f_t1 = self.sigmoid.forward(out[:5, :])
            cc_t1 = self.tanh.forward(out[5:10, :])
            i_t1 = self.sigmoid.forward(out[10:15, :])
            o_t1 = self.sigmoid.forward(out[15:, :])
            
            c_t1 = f_t1*self.prev_c_t1 + i_t1*cc_t1
            a_t1 = o_t1*self.tanh.forward(c_t1)
            
            P_drop = np.random.choice([0, 1], p=[1 - self.Drop, self.Drop])
            if P_drop == 0:
                concat_prev_a_t2_a_t1 = np.concatenate((self.prev_a_t2, a_t1), axis = 0)
            else:
                concat_prev_a_t2_a_t1 = np.concatenate((self.prev_a_t2, np.zeros(a_t1.shape)), axis = 0)
                            
            if self.Drop != 0:
                concat_prev_a_t2_a_t1/=self.Drop
                
            out2 = np.dot(self.W_2, concat_prev_a_t2_a_t1) + self.b_2
            
            f_t2 = self.sigmoid.forward(out[:5 , :])
            cc_t2 = self.tanh.forward(out[5:10 , :])
            i_t2 = self.sigmoid.forward(out[10:15 , :])
            o_t2 = self.sigmoid.forward(out[15: , :])
            
            c_t2 = f_t2*self.prev_c_t2 + i_t2*cc_t2
            a_t2 = o_t2*self.tanh.forward(c_t2)
            
            # backpropagation에서 사용할 정보 저장 (매 layer의 Drop 여부, x_t, prev_a_t1, a_t1, prev_a_t2, a_t2, prev_c_t1, c_t1, prev_c_t2, c_t2, o_t1, o_t2, i_t1, i_t2, cc_t1, cc_t2, f_t1, f_t2)
            self.information.append((P_drop, vec[i].T, self.prev_a_t1, a_t1, self.prev_a_t2, a_t2, self.prev_c_t1, c_t1, self.prev_c_t2, c_t2, o_t1, o_t2, i_t1, i_t2, cc_t1, cc_t2, f_t1, f_t2))
            self.prev_a_t1, self.prev_a_t2, self.prev_c_t1, self.prev_c_t2 = a_t1, a_t2, c_t1, c_t2
            
        out = np.dot(self.W_y, a_t2) + self.b_y
        self.y_t = self.softmax.forward(out,y.T)
        self.GD()
        return self.y_t
    
    def SGD_forward_only(self,x,y):
        vec = np.zeros((10, self.batch_size, len(self.vector[2]['his'])))
        for i in range(self.batch_size):
            for j in range(len(x[i])):
                vec[j,i] = self.vector[2][x[i][j].lower()]
        for i in range(len(x)):
            concat_prev_a_t1_x = np.concatenate((self.prev_a_t1, vec[i].T), axis = 0)
            
            out = np.dot(self.W_1, concat_prev_a_t1_x) + self.b_1
            
            f_t1 = self.sigmoid.forward(out[:5, :])
            cc_t1 = self.tanh.forward(out[5:10, :])
            i_t1 = self.sigmoid.forward(out[10:15, :])
            o_t1 = self.sigmoid.forward(out[15:, :])
            
            c_t1 = f_t1*self.prev_c_t1 + i_t1*cc_t1
            a_t1 = o_t1*self.tanh.forward(c_t1)
            
            P_drop = np.random.choice([0, 1], p=[1 - self.Drop, self.Drop])
            if P_drop == 0:
                concat_prev_a_t2_a_t1 = np.concatenate((self.prev_a_t2, a_t1), axis = 0)
            else:
                concat_prev_a_t2_a_t1 = np.concatenate((self.prev_a_t2, np.zeros(a_t1.shape)), axis = 0)
                
            out2 = np.dot(self.W_2, concat_prev_a_t2_a_t1) + self.b_2
            
            f_t2 = self.sigmoid.forward(out[:5 , :])
            cc_t2 = self.tanh.forward(out[5:10 , :])
            i_t2 = self.sigmoid.forward(out[10:15 , :])
            o_t2 = self.sigmoid.forward(out[15: , :])
            
            c_t2 = f_t2*self.prev_c_t2 + i_t2*cc_t2
            a_t2 = o_t2*self.tanh.forward(c_t2)
            
            self.prev_a_t1, self.prev_a_t2, self.prev_c_t1, self.prev_c_t2 = a_t1, a_t2, c_t1, c_t2
            
        out = np.dot(self.W_y, a_t2) + self.b_y
        return out
        
    def Adam(self, beta1 = 0.9, beta2 = 0.999):
        gradient = self.backward()
        for j in range(100):
            for i in range(len(gradient)):
                self.first_moment[i] = beta1 * self.first_moment[i] + (1-beta1)*gradient[i]
                self.second_moment[i] = beta2 * self.second_moment[i] + (1-beta2)*gradient[i]*gradient[i]
                self.first_unbias[i] = self.first_moment[i] / (1-beta1**self.count)
                self.second_unbias[i] = self.second_moment[i] / (1-beta2**self.count)

                if i == 0:
                    self.W_y -= (self.learning_rate * self.first_unbias[i]/(np.sqrt(self.second_unbias[i]+1e07)))
                elif i == 1:
                    self.b_y -= (self.learning_rate * self.first_unbias[i]/(np.sqrt(self.second_unbias[i]+1e07)))
                elif i == 2:
                    self.W_1 -= (self.learning_rate * self.first_unbias[i]/(np.sqrt(self.second_unbias[i]+1e07)))
                elif i == 3:
                    self.W_2 -= (self.learning_rate * self.first_unbias[i]/(np.sqrt(self.second_unbias[i]+1e07)))
                elif i == 4:
                    self.b_1 -= (self.learning_rate * self.first_unbias[i]/(np.sqrt(self.second_unbias[i]+1e07)))
                elif i == 5:
                    self.b_2 -= (self.learning_rate * self.first_unbias[i]/(np.sqrt(self.second_unbias[i]+1e07)))
            self.count+=1