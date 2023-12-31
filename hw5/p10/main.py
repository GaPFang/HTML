from libsvm.svmutil import *
import numpy as np
import os
import sys
import random
import matplotlib.pyplot as plt

C = [0.01, 0.1, 1, 10, 100]

Eout_fd = open("Eout.txt", "w")
y_train, x_train = svm_read_problem('../train.txt')
y_test, x_test = svm_read_problem('../test.txt')

for i in range(len(y_train)):
    if y_train[i] == 1:
        y_train[i] = 1
    else:
        y_train[i] = -1
train_prob = svm_problem(y_train, x_train)

for i in range(len(y_test)):
    if y_test[i] == 1:
        y_test[i] = 1
    else:
        y_test[i] = -1

min_Eout = 1
min_C = 0
for c in C:
    param = svm_parameter('-s 0 -t 2 -g 1 -q -c ' + str(c))
    m = svm_train(train_prob, param)
    p_labs, p_acc, p_vals = svm_predict(y_test, x_test, m)
    Eout = 0
    for j in range(len(p_labs)):
        if (p_labs[j] * y_test[j] < 0):
            Eout += 1
    Eout /= len(p_labs)
    if Eout < min_Eout:
        min_Eout = Eout
        min_C = c
    Eout_fd.write('C = ' + str(c) + ', Eout = ' + str(Eout) + '\n')

print('lowest Eout is ' + str(min_Eout) + ', C = ' + str(min_C))
Eout_fd.close()

# repeat = 128
# N = 200
# train_data = []
# y_all = []
# z_all = []
# _lambda = [1e-6, 1e-4, 1e-2, 1, 1e2]

# f = open("train.txt", "r")
# for i in range(N):
#     train_data.append(f.readline().split())
#     y_all.append(int(train_data[i][6]))
#     train_data[i][1:7] = train_data[i][0:6]
#     train_data[i][0] = 1
#     z_all.append({})
#     j = 1
#     for a in range(7):
#         for b in range(a, 7):
#             for c in range(b, 7):
#                 tmp = float(train_data[i][a]) * float(train_data[i][b]) * float(train_data[i][c])
#                 z_all[i].update({j:tmp})
#                 j += 1
# f.close()

# best_E_CV = np.ones(repeat)
# best_lambda = np.zeros(repeat)

# f = open("E_in.txt", "w")
# for r in range(repeat):
#     np.random.seed(2 * r)
#     mess = np.random.permutation(N).tolist()
#     fold = [mess[:int(N/5)]] + [mess[int(N/5):int(2 * N/5)]] + [mess[int(2 * N/5):int(3 * N/5)]] + [mess[int(3 * N/5):int(4 * N/5)]] + [mess[int(4 * N/5):N]]
#     E_CV = np.zeros(5).tolist()
#     for i in range(len(_lambda)):
#         _C = 1 / (2 * _lambda[i])
#         param = parameter('-s 0 -c ' + str(_C) + ' -e 0.000001')
#         for v in range(5):
#             y_train = []
#             z_train = []
#             y_val = []
#             z_val = []
#             for j in range(5):
#                 if j == v:
#                     for k in range(int(N/5)):
#                         y_val.append(y_all[fold[j][k]])
#                         z_val.append(z_all[fold[j][k]])
#                 else:
#                     for k in range(int(N/5)):
#                         y_train.append(y_all[fold[j][k]])
#                         z_train.append(z_all[fold[j][k]])
#             print(z_train)
#             prob = problem(y_train, z_train)
#             m = train(prob, param)
#             p_label, p_acc, p_val = predict(y_val, z_val, m)
#             E_CV[i] += ((1 - p_acc[0]) / 100)
#         E_CV[i] /= 5
#         if (E_CV[i] <= best_E_CV[r]):
#             best_E_CV[r] = E_CV[i]
#             best_lambda[r] = _lambda[i]
#     f.write("log_10(lambda*) is " + str(np.log10(best_lambda[r])) + ", E_in is " + str(best_E_CV[r]) + "\n")
# f.close()

# bins = np.linspace(-6.5, 2.5, 10)
# plt.hist(np.log10(best_lambda), bins, label='log_10(lambda*)')
# plt.title('P12: Histogram of log_10(lambda*)')
# plt.xlabel('log_10(lambda*)')
# plt.ylabel('#')
# plt.show()
