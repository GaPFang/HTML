import sys
sys.path.insert(0, "..")
from modules import *

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