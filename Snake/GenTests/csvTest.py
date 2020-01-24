import matplotlib.pyplot as plt
import csv

x = []
y = []
z = []

with open('Gen test - 2019-12-29 - 13:06:11.csv','r') as csvfile:
    plots = csv.reader(csvfile, delimiter='.')
    for row in plots:
        x.append(row[0])
        y.append(row[1])
        z.append(row[2])

plt.plot(x,y,z, label='Loaded from file!')
plt.xlabel('x')
plt.ylabel('y')
plt.ylabel('z')
plt.title('Interesting Graph\nCheck it out')
plt.legend()
plt.show()
