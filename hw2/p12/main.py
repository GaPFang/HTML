import matplotlib.pyplot as plt

Ein = []
Eout = []
for i in range(2000):
    Ein.append(float(input('')))
    Eout.append(float(input('')))
plt.title('Distribution of Ein(g) and Eout(g)')
plt.xlabel('Ein')
plt.ylabel('Eout')
plt.scatter(Ein, Eout)
plt.show()

