#include <stdio.h>
#include <stdlib.h>
#include <math.h>
#include <time.h> 
#include <stdbool.h>
#include <fcntl.h>
#include <unistd.h>
#include <string.h>

#define N 8
#define REPEAT 2000
#define BUFFER_SIZE 60

// void sort(double arr[], int arrSize);

int main() {
    srand(time(NULL));

    char buf[BUFFER_SIZE];
    int outFd = open("out.txt", O_RDWR | O_CREAT | O_TRUNC | O_APPEND, 0666);
    int pyinFd = open("pyin.txt", O_RDWR | O_CREAT | O_TRUNC | O_APPEND, 0666);

    double *Eout_minus_Ein = malloc(sizeof(double) * REPEAT);

    for (int r = 0; r < REPEAT; r++) {
        double x[N];
        int y[N];
        double theta;

        for (int i = 0; i < N; i++) {
            x[i] = (double)rand() / RAND_MAX * 2 - 1;
        }
        // printf("\n(x, y):\n");
        for (int i = 0; i < N; i++) {
            if ((double)rand() / RAND_MAX < 0.9) {
                y[i] = x[i] > 0 ? 1 : (-1);
            } else {
                y[i] = x[i] > 0 ? (-1) : 1;
            }
            // printf("(%lf, %d)\n", x[i], y[i]);
        }
        theta = (double)rand() / RAND_MAX * 2 - 1;
        int s = (double)rand() / RAND_MAX > 0.5 ? 1 : -1;
        double Ein = 0;
        for (int i = 0; i < N; i++) {
            if (y[i] * s * (x[i] - theta) <= 0) Ein += 1;
        }
        Ein /= N;
        double abs_theta = theta > 0 ? theta : -theta;
        double Eout = 0.5 - 0.4 * s + 0.4 * s * abs_theta;
        Eout_minus_Ein[r] = Eout - Ein;
        memset(buf, 0, strlen(buf));
        snprintf(buf, BUFFER_SIZE, "(s, theta, Ein, Eout) = (%d, %lf, %lf, %lf)\n", s, theta, Ein, Eout);
        write(outFd, buf, strlen(buf));
        memset(buf, 0, strlen(buf));
        snprintf(buf, BUFFER_SIZE, "%lf\n%lf\n", Ein, Eout);
        write(pyinFd, buf, strlen(buf));
    }
    sort(Eout_minus_Ein, REPEAT);
    printf("median of (Eout-Ein) = %lf\n", (Eout_minus_Ein[REPEAT / 2] + Eout_minus_Ein[REPEAT / 2 + 1]) / 2);
    return 0;
}

// void sort(double arr[], int arrSize) {
//     for (int i = 1; i < arrSize; i++) {
//         for (int j = 0; j < arrSize - i; j++) {
//             if (arr[j] > arr[j + 1]) {
//                 double tmp = arr[j];
//                 arr[j] = arr[j + 1];
//                 arr[j + 1] = tmp;
//             }
//         }
//     }
// }