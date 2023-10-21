import numpy as np
import matplotlib.pyplot as plt

trainSize = 256
testSize = 4096
repeat = 128

E_in_hist = []
E_out_hist = []

f = open("EinEout.txt", "w")

for r in range(repeat):
    train_y = np.random.randint(2, size = trainSize)
    train_x = []
    for i in range(trainSize):
        train_y[i] = 2 * (train_y[i] - 0.5)
        if train_y[i] == 1:
            x1 = np.random.normal(3, np.sqrt(0.4), 1)
            x2 = np.random.normal(2, np.sqrt(0.4), 1)
            train_x.append([1, x1[0], x2[0]])
        else:
            x1 = np.random.normal(5, np.sqrt(0.6), 1)
            x2 = np.random.normal(0, np.sqrt(0.6), 1)
            train_x.append([1, x1[0], x2[0]])
    H = np.linalg.pinv(train_x)
    w_LIN = np.dot(H, train_y)
    y_hat_in = np.dot(train_x, w_LIN)
    E_in = 0
    for i in range(trainSize):
        if (y_hat_in[i] * train_y[i] < 0):
            E_in += 1
    E_in /= trainSize

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
    y_hat_out = np.dot(test_x, w_LIN)
    E_out = 0
    for i in range(testSize):
        if (y_hat_out[i] * test_y[i] < 0):
            E_out += 1
    E_out /= testSize
    f.write("(E_in, E_out) = (" + str(E_in) + ", " + str(E_out) + ")\n")
    E_in_hist.append(E_in)
    E_out_hist.append(E_out)

f.close()
print("E_in median: " + str(np.median(E_in_hist)))
print("E_out median: " + str(np.median(E_out_hist)))

bins = np.linspace(0, 0.07, 100)
plt.hist(E_in_hist, bins, alpha=0.5, label='E_in')
plt.hist(E_out_hist, bins, alpha=0.5, label='E_out')
plt.legend(loc='upper right')
plt.title('Histogram of E_in and E_out')
plt.show()