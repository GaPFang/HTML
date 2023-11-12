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
    random.seed(r)
    E_CV = []
    for i in range(len(_lambda)):
        _C = 1 / (2 * _lambda[i])
        param = parameter('-s 0 -c ' + str(_C) + ' -e 0.000001 -v 5')
        prob = problem(y_all, z_all)
        CV_ACC = train(prob, param)
        E_CV.append((1 - CV_ACC) / 100)
        if (E_CV[i] <= best_E_CV[r]):
            best_E_CV[r] = E_CV[i]
            best_lambda[r] = _lambda[i]
    f.write("log_10(lambda*) is " + str(np.log10(best_lambda[r])) + ", E_in is " + str(best_E_CV[r]) + "\n")
f.close()

bins = np.linspace(-6.5, 2.5, 10)
plt.hist(np.log10(best_lambda), bins, label='log_10(lambda*)')
plt.title('P12: Histogram of log_10(lambda*)')
plt.show()