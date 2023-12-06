import numpy as np
from libsvm.svmutil import *
import copy

class Node:
    def __init__(self):
        self.theta = None
        self.feature = None
        self.value = None
        self.left = None
        self.right = None

# def sortFeature(x, y):
#     sorted_data = sorted(zip(x, y), key=lambda pair: pair[0])
#     sorted_x, sorted_y = zip(*sorted_data)
#     sorted_x = list(sorted_x)
#     sorted_y = list(sorted_y)
#     return sorted_x, sorted_y

def getTheta(x):
    sortedFeature = []
    for i in range(len(x)):
        for j in range(len(x[i])):
            if i == 0:
                sortedFeature.append([])
            sortedFeature[j].append(x[i][j])
    for i in range(len(sortedFeature)):
        sortedFeature[i] = np.sort(sortedFeature[i])
    theta = []
    for i in range(len(sortedFeature)):
        theta.append([])
        for j in range(len(sortedFeature[i]) - 1):
            if sortedFeature[i][j] != sortedFeature[i][j + 1]:
                theta[i].append((sortedFeature[i][j] + sortedFeature[i][j + 1]) / 2)
    return theta

def impurity(y):
    # if len(y) == 0:
    #     return 0
    average = np.mean(y)
    error = np.sum((y - average) ** 2) / len(y)
    return error

def CandRT_train(train_x, train_y, theta):
    endFlag = True
    for i in range(len(train_y) - 1):
        if train_y[i] != train_y[i + 1]:
            endFlag = False
            break
    if endFlag:
        node = Node()
        node.value = train_y[0]
        return node
    minImpurity = None
    bestTheta = None
    bestFeature = None
    min_x = []
    max_x = []
    for i in range(len(train_x[0])):
        min_x.append(min(train_x, key=lambda x: x[i])[i])
        max_x.append(max(train_x, key=lambda x: x[i])[i])
    for i in range(len(theta)):
        for j in range(len(theta[i])):
            left_y = []
            right_y = []
            if theta[i][j] < min_x[i] or theta[i][j] > max_x[i]:
                continue
            for k in range(len(train_y)):
                if train_x[k][i] < theta[i][j]:
                    left_y.append(train_y[k])
                else:
                    right_y.append(train_y[k])
            impurity_all = impurity(left_y) * len(left_y) + impurity(right_y) * len(right_y)
            if minImpurity == None or impurity_all < minImpurity:
                minImpurity = impurity_all
                bestTheta = theta[i][j]
                bestFeature = i
    left_x = []
    left_y = []
    right_x = []
    right_y = []
    for i in range(len(train_x)):
        if train_x[i][bestFeature] < bestTheta:
            left_x.append(train_x[i])
            left_y.append(train_y[i])
        else:
            right_x.append(train_x[i])
            right_y.append(train_y[i])
    root = Node()
    root.theta = bestTheta
    root.feature = bestFeature
    root.left = CandRT_train(left_x, left_y, theta)
    root.right = CandRT_train(right_x, right_y, theta)
    return root

def CandRT_predict(root, x):
    if root.value != None:
        return root.value
    if x[root.feature] < root.theta:
        return CandRT_predict(root.left, x)
    else:
        return CandRT_predict(root.right, x)

def squareLoss(pred_y, test_y):
    loss = 0
    for i in range(len(pred_y)):
        loss += (pred_y[i] - test_y[i]) ** 2
    return loss / len(pred_y)

def main():
    train_y, train_x = svm_read_problem('../train.txt')
    test_y, test_x = svm_read_problem('../test.txt')
    for i in range(len(train_x)):
        train_x[i] = list(train_x[i].values())
    for i in range(len(test_x)):
        test_x[i] = list(test_x[i].values())
    # train_x = train_x[:1600]
    # train_y = train_y[:1600]
    theta = getTheta(train_x)
    root = CandRT_train(train_x, train_y, theta)
    pred_y = []
    for i in range(len(train_x)):
        pred_y.append(CandRT_predict(root, train_x[i]))
    print("Ein =", squareLoss(pred_y, train_y))
    pred_y = []
    for i in range(len(test_x)):
        pred_y.append(CandRT_predict(root, test_x[i]))
    print("Eout =", squareLoss(pred_y, test_y))
    
    

if __name__ == '__main__':
    main()
    
