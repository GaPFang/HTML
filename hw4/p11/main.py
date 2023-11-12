from liblinear.liblinearutil import *
import numpy as np
import os
import sys
import random
import matplotlib.pyplot as plt

repeat = 128
N = 200
D_train_size = 120
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

best_E_val = np.ones(repeat)
best_lambda = np.zeros(repeat)

f = open("E_in.txt", "w")
for r in range(repeat):
    random.seed(r)
    sample = random.sample(range(N), D_train_size)
    # sample.sort()
    y_train = []
    y_val = []
    z_train = []
    z_val = []
    for i in range(N):
        if i in sample:
            y_train.append(y_all[i])
            z_train.append(z_all[i])
        else:
            y_val.append(y_all[i])
            z_val.append(z_all[i])
    E_val = []
    for i in range(len(_lambda)):
        _C = 1 / (2 * _lambda[i])
        param = parameter('-s 0 -c ' + str(_C) + ' -e 0.000001')
        prob = problem(y_train, z_train)
        m = train(prob, param)
        p_label, p_acc, p_val = predict(y_val, z_val, m)
        E_val.append((100 - p_acc[0]) / 100)
        if (E_val[i] < best_E_val[r]):
            best_E_val[r] = E_val[i]
            best_lambda[r] = _lambda[i]
    f.write("log_10(lambda*) is " + str(np.log10(best_lambda[r])) + ", E_in is " + str(best_E_val[r]) + "\n")
f.close()

bins = np.linspace(-6.5, 2.5, 10)
plt.hist(np.log10(best_lambda), bins, label='log_10(lambda*)')
plt.title('P11: Histogram of log_10(lambda*)')
plt.show()