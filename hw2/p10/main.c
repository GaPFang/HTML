#include <stdio.h>
#include <stdlib.h>
#include <math.h>
#include <time.h> 
#include <stdbool.h>
#include <fcntl.h>
#include <unistd.h>
#include <string.h>

#define N 32
#define REPEAT 2000
#define BUFFER_SIZE 60

void sort(double arr[], int arrSize);

int main() {
    srand(time(NULL));

    char buf[BUFFER_SIZE];
    int outFd = open("out.txt", O_RDWR | O_CREAT | O_TRUNC | O_APPEND, 0666);
    int pyinFd = open("pyin.txt", O_RDWR | O_CREAT | O_TRUNC | O_APPEND, 0666);

    double *Eout_minus_Ein = malloc(sizeof(double) * REPEAT);

    for (int r = 0; r < REPEAT; r++) {
        double x[N], theta[N];
        int y[N];
        double min_Ein = N;
        int min_s = 1;
        double min_theta = 1;

        for (int i = 0; i < N; i++) {
            x[i] = (double)rand() / RAND_MAX * 2 - 1;
        }
        sort(x, N);
        // printf("\n(x, y):\n");
        for (int i = 0; i < N; i++) {
            if ((double)rand() / RAND_MAX < 0.9) {
                y[i] = x[i] > 0 ? 1 : (-1);
            } else {
                y[i] = x[i] > 0 ? (-1) : 1;
            }
            // printf("(%lf, %d)\n", x[i], y[i]);
        }
        theta[0] = -1;
        // printf("\ntheta: %lf ", theta[0]);
        for (int i = 0; i < N - 1; i++) {
            theta[i + 1] = (x[i] != x[i + 1]) ? (x[i] + x[i + 1]) / 2 : (-1);
            // printf("%lf ", theta[i + 1]);
        }
        // printf("\n");
        for (int i = 0; i < N; i++) {
            int Ein[2] = {0, 0}; // s = -1, 1
            for (int j = 0; j < N; j++) {
                if (x[j] > theta[i]) {
                    if (y[j] == 1) {
                        Ein[0] += 1;
                    } else {
                        Ein[1] += 1;
                    }
                } else {
                    if (y[j] == 1) {
                        Ein[1] += 1;
                    } else {
                        Ein[0] += 1;
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
            // printf("%d %d\n", Ein[0], Ein[1]);
        }
        min_Ein /= N;
        double abs_min_theta = min_theta > 0 ? min_theta : -min_theta;
        double Eout = 0.5 - 0.4 * min_s + 0.4 * min_s * abs_min_theta;
        Eout_minus_Ein[r] = Eout - min_Ein;
        memset(buf, 0, strlen(buf));
        sprintf(buf, "(s, theta, Ein, Eout) = (%d, %lf, %lf, %lf)\n", min_s, min_theta, min_Ein, Eout);
        write(outFd, buf, strlen(buf));
        memset(buf, 0, strlen(buf));
        sprintf(buf, "%lf\n%lf\n", min_Ein, Eout);
        write(pyinFd, buf, strlen(buf));
    }
    sort(Eout_minus_Ein, REPEAT);
    printf("median of (Eout-Ein) = %lf\n", (Eout_minus_Ein[REPEAT / 2] + Eout_minus_Ein[REPEAT / 2 + 1]) / 2);
    return 0;
}

void sort(double arr[], int arrSize) {
    for (int i = 1; i < arrSize; i++) {
        for (int j = 0; j < arrSize - i; j++) {
            if (arr[j] > arr[j + 1]) {
                double tmp = arr[j];
                arr[j] = arr[j + 1];
                arr[j + 1] = tmp;
            }
        }
    }
}