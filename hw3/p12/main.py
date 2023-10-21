import numpy as np
import matplotlib.pyplot as plt

trainSize = 256 + 16
testSize = 4096
repeat = 128
T = 500
eta = 0.1

f = open("out.txt", "w")

E_LIN_out = []
E_LOG_out = []

def log_fn(ys):
    return (1 / (1 + np.exp(-ys)))

def gra_Ein(y, w, x):
    x = np.array(x)
    gra_E_in = np.zeros(3)
    for i in range(trainSize):
        gra_E_in += log_fn(-y[i] * np.dot(w, x[i])) * (-y[i] * x[i])
    gra_E_in /= trainSize
    return gra_E_in

for r in range(repeat):
    train_y = np.concatenate([np.random.randint(2, size = trainSize - 16), np.ones(16)])
    train_x = []
    for i in range(trainSize - 16):
        train_y[i] = 2 * (train_y[i] - 0.5)
        if train_y[i] == 1:
            x1 = np.random.normal(3, np.sqrt(0.4), 1)
            x2 = np.random.normal(2, np.sqrt(0.4), 1)
            train_x.append([1, x1[0], x2[0]])
        else:
            x1 = np.random.normal(5, np.sqrt(0.6), 1)
            x2 = np.random.normal(0, np.sqrt(0.6), 1)
            train_x.append([1, x1[0], x2[0]])
    for i in range(16):
        x1 = np.random.normal(0, np.sqrt(0.1), 1)
        x2 = np.random.normal(6, np.sqrt(0.3), 1)
        train_x.append([1, x1[0], x2[0]])
            
    H = np.linalg.pinv(train_x)
    w_LIN = np.dot(H, train_y)

    w_LOG = np.zeros(3)
    for t in range(T):
        w_LOG -= eta * gra_Ein(train_y, w_LOG, train_x)
        # print(w_LOG)

    test_y = np.random.randint(2, size = testSize)
    test_x = []
    for i in range(testSize):
        test_y[i] = 2 * (test_y[i] - 0.5)
        if test_y[i] == 1:
            x1 = np.random.normal(3, np.sqrt(0.4), 1)
            x2 = np.random.normal(2, np.sqrt(0.4), 1)
            test_x.append([1, x1[0], x2[0]])
        else:
            x1 = np.random.normal(5, np.sqrt(0.6), 1)
            x2 = np.random.normal(0, np.sqrt(0.6), 1)
            test_x.append([1, x1[0], x2[0]])

    y_LIN = np.dot(test_x, w_LIN)
    E_LIN = 0
    for i in range(testSize):
        if (y_LIN[i] * test_y[i] < 0):
            E_LIN += 1
    E_LIN /= testSize

    y_LOG = np.dot(test_x, w_LOG)
    E_LOG = 0
    for i in range(testSize):
        if (y_LOG[i] * test_y[i] < 0):
            E_LOG += 1
    E_LOG /= testSize

    f.write("(w_LIN, w_LOG, E_out(linear), E_out(logistic)) = (" + str(w_LIN) + ", " + str(w_LOG) + ", " + str(E_LIN) + ", " + str(E_LOG) + ")\n")
    E_LIN_out.append(E_LIN)
    E_LOG_out.append(E_LOG)

f.close()
print("E_out(linear) median: " + str(np.median(E_LIN_out)))
print("E_out(logistic) median: " + str(np.median(E_LOG_out)))

plt.scatter(E_LIN_out, E_LOG_out)
plt.title('Histogram of Eout(linear) and Eout(logistic)')
plt.xlabel("E_out(linear)")
plt.ylabel("E_out(logistic)")
plt.show()