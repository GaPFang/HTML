#include <stdio.h>
#include <stdlib.h>
#include <math.h>
#include <time.h> 

typedef struct node {
    int updates, count;
    struct node *larger, *smaller;
} node;

int main() {
    srand(time(NULL));
    int N = 256;
    int largestUpdates;
    double data[256][13];
    int y[256];
    for (int i = 0; i < N; i++) {
        data[i][0] = 1;
        double mag = 1;
        for (int j = 1; j <= 12; j++) {
            scanf("%lf", &data[i][j]);
            mag += data[i][j] * data[i][j];
        }
        mag = sqrt(mag);
        for (int j = 0; j <= 12; j++) {
            data[i][j] /= mag;
        }
        scanf("%d", &y[i]);
    }
    double w[13];
    node *head = NULL;
    int repeat = 1000;
    for (int k = 1; k <= repeat; k++) {
        int totalUpdates = 0;
        int correctCount = 0;
        for (int i = 0; i < 13; i++) {
            w[i] = 0;
        }
        while (correctCount < 5 * N) {
            correctCount += 1;
            int randInt = (double)rand() / (RAND_MAX + 1.0) * 256;
            int inner = 0;
            for (int i = 0; i < 13; i++) {
                inner += w[i] * data[randInt][i];
            }
            if (inner * y[randInt] < 0 || (inner == 0 && y[randInt] == 1)) {
                for (int i = 0; i < 13; i++) {
                    w[i] += y[randInt] * data[randInt][i];
                }
                correctCount = 0;
                totalUpdates += 1;
            }
        }
        fprintf(stderr, "w_PLA_%d = (%lf, %lf, %lf, %lf, %lf, %lf, %lf, %lf, %lf, %lf, %lf, %lf, %lf)\n", k, w[0], w[1], w[2], w[3], w[4], w[5], w[6], w[7], w[8], w[9], w[10], w[11], w[12]);
        if (head == NULL) {
            head = malloc(sizeof(node));
            head -> updates = totalUpdates;
            head -> count = 1;
            head -> larger = NULL;
            head -> smaller = NULL;
            largestUpdates = totalUpdates;
        } else {
            node *cur = head;
            while (cur -> larger && cur -> updates < totalUpdates) {
                cur = cur -> larger;
            }
            if (cur -> updates == totalUpdates) {
                cur -> count++;
            } else if (cur -> updates > totalUpdates) {
                node *tmp = malloc(sizeof(node));
                tmp -> updates = totalUpdates;
                tmp -> count = 1;
                tmp -> larger = cur;
                tmp -> smaller = cur -> smaller;
                if (cur == head) {
                    head = tmp;
                } else {
                    cur -> smaller -> larger = tmp;
                }
                cur -> smaller = tmp;
            } else {
                node *tmp = malloc(sizeof(node));
                tmp -> updates = totalUpdates;
                tmp -> count = 1;
                tmp -> larger = NULL;
                tmp -> smaller = cur;
                cur -> larger = tmp;
                largestUpdates = totalUpdates;
            }
        }
    }
    int smallestUpdates = head -> updates;
    int total = 0;
    total += head -> updates * head -> count;
    printf("%d\n%d\n", smallestUpdates, largestUpdates);
    printf("%d\n", head -> count);
    node *cur = head -> larger;
    int lastUpdates = head -> updates;
    while (cur) {
        for (int i = 0; i < cur -> updates - lastUpdates - 1; i++) {
            printf("0\n");
        }
        printf("%d\n", cur -> count);
        lastUpdates = cur -> updates;
        total += cur -> updates * cur -> count;
        cur = cur -> larger;
    }
    printf("%lf\n", (double)total / 1000);
    return 0;
}