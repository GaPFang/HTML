#include <stdio.h>
#include <stdlib.h>
#include <math.h>
#include <time.h> 
#include <stdbool.h>

#define N 32

void sort(double x[]);

int main() {
    srand(time(NULL));
    int repeat = 1;
    while (repeat--) {
        double x[N], theta[N];
        int y[N];
        int min_Ein = N;
        int min_s = 1;
        double min_theta = 1;
        for (int i = 0; i < N; i++) {
            x[i] = (double)rand() / RAND_MAX * 2 - 1;
        }
        sort(x);
        for (int i = 0; i < N; i++) {
            if ((double)rand() / RAND_MAX > 0.9) {
                y[i] = (x[i] > 0 ? 1 : (-1)) * (-1);
            } else {
                y[i] = x[i] > 0 ? 1 : (-1);
            }
        }
        theta[0] = -1;
        for (int i = 0; i < N - 1; i++) {
            theta[i + 1] = (x[i] != x[i + 1]) ? (x[i] + x[i + 1]) / 2 : (-1);
        }
        for (int i = 0; i < N; i++) {
            int Ein[2] = {0, 0};
            for (int j = 0; j < N; j++) {
                if (x[j] > theta[i]) {
                    if (y[j] == 1) {
                        Ein[0]++;
                    } else {
                        Ein[1]++;
                    }
                } else {
                    if (y[j] == 1) {
                        Ein[1]++;
                    } else {
                        Ein[0]++;
                    }
                }
            }
            if (Ein[0] < min_Ein || ((Ein[0] == min_Ein) && ((-1) * theta[i] < min_s * min_theta))) {
                min_Ein = Ein[0];
                min_s = -1;
                min_theta = theta[i];
            }
            if (Ein[1] < min_Ein || ((Ein[1] == min_Ein) && (theta[i] < min_s * min_theta))) {
                min_Ein = Ein[1];
                min_s = 1;
                min_theta = theta[i];
            }
        }
        double min_Eout = 0.5 - 0.4 * min_s + 0.4 * min_s * abs(min_theta);
        printf("(s, theta, Ein, Eout) = (%d, %lf, %d, %lf)", min_s, min_theta, min_Ein, min_Eout);
    }
    return 0;
}

void sort(double x[]) {
    for (int i = 1; i < N; i++) {
        for (int j = 0; j < N - i; j++) {
            if (x[j] > x[j + 1]) {
                double tmp = x[j];
                x[j] = x[j + 1];
                x[j + 1] = tmp;
            }
        }
    }
}