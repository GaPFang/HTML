from liblinear.liblinearutil import *
import numpy as np
import os
import sys

train_data = []
y = []
z = []
_lambda = [1e-6, 1e-4, 1e-2, 1, 1e2]

outFd = open("stdout.txt", "w")
os.dup2(outFd.fileno(), 1)

f = open("train.txt", "r")
for i in range(200):
    train_data.append(f.readline().split())
    y.append(int(train_data[i][6]))
    train_data[i][1:7] = train_data[i][0:6]
    train_data[i][0] = 1
    z.append({})
    j = 1
    for a in range(7):
        for b in range(a, 7):
            for c in range(b, 7):
                tmp = float(train_data[i][a]) * float(train_data[i][b]) * float(train_data[i][c])
                z[i].update({j:tmp})
                j += 1
f.close()

prob = problem(y, z)

best_E_in = 1
E_in = []

for i in range(len(_lambda)):
    _C = 1 / (2 * _lambda[i])
    param = parameter('-s 0 -c ' + str(_C) + ' -e 0.000001')
    m = train(prob, param)
    p_label, p_acc, p_val = predict(y, z, m)
    E_in.append((100 - p_acc[0]) / 100)
    if (E_in[i] <= best_E_in):
        best_E_in = E_in[i]
        best_lambda = _lambda[i]
f = open("E_in.txt", "w")
f.write("E_in(lambda=" + str(_lambda)[1:-1] + ")=" + str(E_in)[1:-1] + '\n')
f.close()

print("lambda* is " + str(best_lambda) + ", log_10(lambda*) is " + str(np.log10(best_lambda)) + ", E_in is " + str(best_E_in), file=sys.stderr)