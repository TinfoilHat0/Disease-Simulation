import csv
import os, sys
import matplotlib.pyplot as plt
import glob

#1. Read simulation logs from folder
path = sys.argv[1]
nFile = 0
logs = []
for filename in glob.glob(os.path.join(path, '*.txt')):
    log = []
    reader = csv.reader(open(filename, 'r'))
    for row in reader:
        log.append(row)
    logs.append(log)
    nFile += 1

#2. Get timesteps, # of infected, # of susceptibles
time = []
avgNSusceptible = []
avgNInfected = []
for log in logs:
    for i in range(0, nFile):
        time.append(int(item[0]))
        nSusceptible.append(int(item[1]))
        nInfected.append(int(item[2]))
        tSim += 1


#3. Plot data
plt.plot(time, avgNInfected)
plt.ylim((0, 700))
plt.ylabel('Number of infected nodes')
plt.title(log[0])
plt.show()
