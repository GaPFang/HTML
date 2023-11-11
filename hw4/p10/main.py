from liblinear.liblinearutil import *
import numpy as np

train_data = []
x = []
y = []
z_dict = []
z_list = []
_lambda = [1e-6, 1e-4, 1e-2, 1, 1e2]

train_input = open("train.txt", "r")
for i in range(200):
    train_data.append(train_input.readline().split())
    x.append(train_data[i][1:7])
    y.append(int(train_data[i][6]))
    train_data[i][1:7] = train_data[i][0:6]
    train_data[i][0] = 1
    for j in range(1, 7):
        x.append(float(train_data[i][j]))
    z_dict.append({})
    z_list.append([])
    j = 1
    for a in range(7):
        for b in range(a, 7):
            for c in range(b, 7):
                tmp = float(train_data[i][a]) * float(train_data[i][b]) * float(train_data[i][c])
                z_dict[i].update({j:tmp})
                z_list[i].append(tmp)
                j += 1

prob = problem(y, z_dict)

best_E_in = 1

f = open("E_in.txt", "w")
for i in range(len(_lambda)):
    _C = 1 / (2 * _lambda[i])
    param = parameter('-s 0 -c ' + str(_C) + ' -e 0.000001')
    m = train(prob, param)
    save_model("w_log_lambda=" + str(_lambda[i]) + ".model", m)
    f1 = open("w_log_lambda=" + str(_lambda[i]) + ".model", "r")
    for j in range(6):
        f1.readline()
    w_log = []
    for j in range(84):
        w_log.append(float(f1.readline()))
    y_log = []
    E_in = 0
    for j in range(len(z_list)):
        y_log.append(np.dot(z_list[j], w_log))
        if (y_log[j] * y[j] < 0):
            E_in += 1
    E_in /= len(z_list)
    if (E_in < best_E_in):
        best_E_in = E_in
        best_lambda = _lambda[i]
    f.write("E_in(lambda=" + str(_lambda[i]) + ")=" + str(E_in) + '\n')

print("lambda* is " + str(best_lambda) + ", log_10(lambda*) is " + str(np.log10(best_lambda)) + ", E_in is " + str(best_E_in))
        