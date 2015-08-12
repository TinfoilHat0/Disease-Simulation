import csv
import os, sys
import matplotlib.pyplot as plt
import glob
import numpy as np

#1. Read simulation logs from folder
path = sys.argv[1]
nFile = 0
logs = []
header = []
for file in glob.glob(path + "/*.txt"):
    log = np.loadtxt(open(file,"rb"),delimiter=",",skiprows=2)
    logs.append(log)
    nFile +=1

#2. Average the numbers
avgLog = np.zeros(shape=log.shape)
for log in logs:
    avgLog += log
avgLog /= nFile

#3. Get timesteps, avg. # of infected, avg. # of susceptibles
time = []
avgNSusceptible = []
avgNInfected = []
for item in avgLog:
    time.append(int(item[0]))
    avgNSusceptible.append(int(item[1]))
    avgNInfected.append(int(item[2]))

#4. Plot data
plt.plot(time, avgNInfected)
plt.ylabel('Number of infected nodes')
#plt.title(log[0])
plt.show()
