import matplotlib.pyplot as plt

smallest = int(input(''))
largest = int(input(''))
axis = []
pyin = []
for i in range(smallest, largest + 1):
    axis.append(i)
    pyin.append(int(input('')))
median = input('')
averageCheck = input('')
print("median number:" + median)
print("average check:" + averageCheck)
plt.bar(axis, pyin)
plt.title('Distribution of The Number of Updates')
plt.xlabel("number of updates")
plt.ylabel("count")
plt.show()

