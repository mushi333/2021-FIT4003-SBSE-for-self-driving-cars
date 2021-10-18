import csv

from matplotlib import pyplot as plt

with open('progress.csv') as csv_file:
    csv_reader = csv.reader(csv_file, delimiter=',')
    rewards = []
    iterations = []
    for (i, row) in enumerate(csv_reader):
        if i == 0:
            entry_dict = {}
            for index in range(len(row)):
                entry_dict[row[index]] = index
            # print(entry_dict)
        else:

            current_reward = [float(row[0]), float(row[1]), float(row[2]), float(row[3]), float(row[4]), float(row[5]),
                              float(row[6]), float(row[7]), float(row[8]), float(row[9])]
            print(current_reward)
            rewards.append(float(row[9]))
            iterations.append(row[10])
            pass
fig = plt.figure()
plt.scatter(iterations, rewards)
plt.xlabel('Step Number')
plt.ylabel('Max Reward')
fig.savefig('test.pdf')
plt.close(fig)
