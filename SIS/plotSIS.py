import csv
import os, sys
import matplotlib.pyplot as plt
import glob

#1. Read simulation logs from folder
path = sys.argv[1]
nFile = 0
log = []
f = open(path, 'rb')
reader = csv.reader(f)
for row in reader:
    log.append(row)

#2. Get timesteps, # of infected, # of susceptibles
time = []
nSusceptible = []
nInfected = []
for item in log[2:]:
    time.append(int(item[0]))
    nSusceptible.append(int(item[1]))
    nInfected.append(int(item[2]))

#3. Plot data
plt.plot(time, nInfected)
plt.ylim((0, 700))
plt.ylabel('Number of infected nodes')
plt.title(log[0])
plt.show()
