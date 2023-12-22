import random
import matplotlib.pyplot as plt
import sys
import os
sys.path.insert(0, "..")
from modules import *

repeat = 2000
fork = 40

def main():
    y_all, x_all = svm_read_problem('../train.txt')
    test_y, test_x = svm_read_problem('../test.txt')
    for i in range(len(x_all)):
        x_all[i] = list(x_all[i].values())
    for i in range(len(test_x)):
        test_x[i] = list(test_x[i].values())
    pred_y_in = []
    pred_y_out = []
    for f in range(fork):
        pid = os.fork()
        if pid != 0:
            continue
        for r in range(int(repeat / fork)):
            random.seed(r + f * int(repeat / fork))
            x_train = []
            y_train = []
            for i in range(int(len(y_all) / 2)):
                index = random.randint(0, len(y_all) - 1)
                x_train.append(x_all[index])
                y_train.append(y_all[index])
            theta = getTheta(x_train)
            root = CandRT_train(x_train, y_train, theta)
            pred_y_in.append([])
            for i in range(len(x_all)):
                pred_y_in[r].append(CandRT_predict(root, x_all[i]))
            pred_y_out.append([])
            for i in range(len(test_x)):
                pred_y_out[r].append(CandRT_predict(root, test_x[i]))
        with open('p10_11_12_' + str(f) + '.txt', 'w') as fd:
            for i in range(int(repeat / fork)):
                print(pred_y_in[i], file=fd)
            for i in range(int(repeat / fork)):
                print(pred_y_out[i], file=fd)
        os._exit(0)
    for f in range(fork):
        os.wait()
    pred_y_in = []
    pred_y_out = []
    for f in range(fork):
        with open('p10_11_12_' + str(f) + '.txt', 'r') as fd:
            for i in range(int(repeat / fork)):
                line = fd.readline().replace('\n', '').replace('[', '').replace(']', '').split(', ')
                pred_y_in.append([])
                for j in range(len(line)):
                    pred_y_in[f * int(repeat / fork) + i].append(float(line[j]))
            for i in range(int(repeat / fork)):
                line = fd.readline().replace('\n', '').replace('[', '').replace(']', '').split(', ')
                pred_y_out.append([])
                for j in range(len(line)):
                    pred_y_out[f * int(repeat / fork) + i].append(float(line[j]))
    pred_y_in_G = []
    pred_y_out_G = []
    pred_y_out_g_t = []
    pred_y_out_G_t = []
    Ein_g = []
    Eout_g = []
    Eout_g_t = []
    Eout_G_t = []
    for t in range(repeat):
        Ein_g.append(squareLoss(pred_y_in[t], y_all))
        Eout_g.append(squareLoss(pred_y_out[t], test_y))
        pred_y_out_g_t.append([])
        pred_y_out_G_t.append([])
        for i in range(len(test_x)):
            pred_y_out_g_t[t].append(pred_y_out[t][i])
            pred_y_out_G_t[t].append(sum([pred_y_out[r][i] for r in range(t + 1)]) / (t + 1))
        Eout_g_t.append(squareLoss(pred_y_out_g_t[t], test_y))
        Eout_G_t.append(squareLoss(pred_y_out_G_t[t], test_y))
    for i in range(len(x_all)):
        pred_y_in_G.append(sum([pred_y_in[r][i] for r in range(repeat)]) / repeat)
    for i in range(len(test_x)):
        pred_y_out_G.append(sum([pred_y_out[r][i] for r in range(repeat)]) / repeat)
    Ein_G = squareLoss(pred_y_in_G, y_all)
    Eout_G = squareLoss(pred_y_out_G, test_y)

    plt.title('p10: Histogram of Eout')
    plt.hist(Eout_g, bins=10)
    plt.xlabel('Eout')
    plt.ylabel('#')
    plt.savefig('p10.png')
    plt.clf()

    plt.title('p11: Scatter of Ein & Eout of g & G')
    plt.scatter(Ein_g, Eout_g, s=1)
    plt.scatter(Ein_G, Eout_G, s=10, c='r')
    plt.legend(['g', 'G'])
    plt.xlabel('Ein')
    plt.ylabel('Eout')
    plt.savefig('p11.png')
    plt.clf()

    plt.title('p12: diagram of Eout_t vs t')
    plt.plot([t + 1 for t in range(repeat)], Eout_g_t)
    plt.plot([t + 1 for t in range(repeat)], Eout_G_t, c='r')
    plt.legend(['g', 'G'])
    plt.xlabel('t')
    plt.ylabel('Eout_t')
    plt.savefig('p12.png')
    plt.clf()

if __name__ == '__main__':
    main()