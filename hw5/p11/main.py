from libsvm.svmutil import *
import numpy as np
import os
import sys
import random
import matplotlib.pyplot as plt

f = open("/dev/null", "w")
os.dup2(f.fileno(), sys.stdout.fileno())
f.close()
C = [0.01, 0.1, 1, 10, 100]
repeat = 1000

y_all, x_all = svm_read_problem('../train.txt')
array = [i for i in range(len(y_all))]

for i in range(len(y_all)):
    if y_all[i] == 1:
        y_all[i] = 1
    else:
        y_all[i] = -1

min_C_arr = {}
for c in C:
    min_C_arr.update({str(c): 0})

for r in range(repeat):
    random.seed(r)
    sample = random.sample(array, 200)
    x_train = []
    x_val = []
    y_train = []
    y_val = []
    for i in range(len(y_all)):
        if i in sample:
            x_val.append(x_all[i])
            y_val.append(y_all[i])
        else:
            x_train.append(x_all[i])
            y_train.append(y_all[i])
    min_Eval = 1
    min_C = 0
    for c in C:
        param = svm_parameter('-s 0 -t 2 -g 1 -q -c ' + str(c))
        train_prob = svm_problem(y_train, x_train)
        m = svm_train(train_prob, param)
        p_labs, p_acc, p_vals = svm_predict(y_val, x_val, m)
        Eval = 0
        for j in range(len(p_labs)):
            if (p_labs[j] * y_val[j] < 0):
                Eval += 1
        Eval /= len(p_labs)
        if Eval < min_Eval:
            min_Eval = Eval
            min_C = c
    min_C_arr[str(min_C)] += 1
for c in C:
    min_C_arr[str(c)] /= repeat

print("C_frequency = " + str(min_C_arr), file=sys.stderr)
plt.bar(list(min_C_arr.keys()), list(min_C_arr.values()))
plt.xlabel("C*")
plt.ylabel("frequency")
plt.title("bar chart of C versus its selection frequency")
plt.show()