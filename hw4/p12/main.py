from liblinear.liblinearutil import *
import numpy as np
import os
import sys
import random
import matplotlib.pyplot as plt

repeat = 128
N = 200
train_data = []
y_all = []
z_all = []
_lambda = [1e-6, 1e-4, 1e-2, 1, 1e2]

outFd = open("stdout.txt", "w")
os.dup2(outFd.fileno(), 1)

f = open("train.txt", "r")
for i in range(N):
    train_data.append(f.readline().split())
    y_all.append(int(train_data[i][6]))
    train_data[i][1:7] = train_data[i][0:6]
    train_data[i][0] = 1
    z_all.append({})
    j = 1
    for a in range(7):
        for b in range(a, 7):
            for c in range(b, 7):
                tmp = float(train_data[i][a]) * float(train_data[i][b]) * float(train_data[i][c])
                z_all[i].update({j:tmp})
                j += 1
f.close()

best_E_CV = np.ones(repeat)
best_lambda = np.zeros(repeat)

f = open("E_in.txt", "w")
for r in range(repeat):
    np.random.seed(2 * r)
    mess = np.random.permutation(N).tolist()
    fold = [mess[:int(N/5)]] + [mess[int(N/5):int(2 * N/5)]] + [mess[int(2 * N/5):int(3 * N/5)]] + [mess[int(3 * N/5):int(4 * N/5)]] + [mess[int(4 * N/5):N]]
    E_CV = np.zeros(5).tolist()
    for i in range(len(_lambda)):
        _C = 1 / (2 * _lambda[i])
        param = parameter('-s 0 -c ' + str(_C) + ' -e 0.000001')
        for v in range(5):
            y_train = []
            z_train = []
            y_val = []
            z_val = []
            for j in range(5):
                if j == v:
                    for k in range(int(N/5)):
                        y_val.append(y_all[fold[j][k]])
                        z_val.append(z_all[fold[j][k]])
                else:
                    for k in range(int(N/5)):
                        y_train.append(y_all[fold[j][k]])
                        z_train.append(z_all[fold[j][k]])
            print(z_train)
            prob = problem(y_train, z_train)
            m = train(prob, param)
            p_label, p_acc, p_val = predict(y_val, z_val, m)
            E_CV[i] += ((1 - p_acc[0]) / 100)
        E_CV[i] /= 5
        if (E_CV[i] <= best_E_CV[r]):
            best_E_CV[r] = E_CV[i]
            best_lambda[r] = _lambda[i]
    f.write("log_10(lambda*) is " + str(np.log10(best_lambda[r])) + ", E_in is " + str(best_E_CV[r]) + "\n")
f.close()

bins = np.linspace(-6.5, 2.5, 10)
plt.hist(np.log10(best_lambda), bins, label='log_10(lambda*)')
plt.title('P12: Histogram of log_10(lambda*)')
plt.xlabel('log_10(lambda*)')
plt.ylabel('#')
plt.show()
