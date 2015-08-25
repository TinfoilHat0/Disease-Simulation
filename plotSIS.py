import csv
import os, sys
import matplotlib.pyplot as plt
import glob
import numpy as np


def plotPrevalance(path):
    folders = [x[0] for x in os.walk(path)]
    prevalance, spreadingRate = [], []
    #1.Go and calculate avg values for each subfolder
    for folder in folders[1:]:
        nFile, logs, header, dimension = 0, [], "", None
        for file in glob.glob(folder + "/*.txt"):
            f = open(file, "rb")
            if len(header) == 0:
                header = f.readline()
            log = np.loadtxt(f, delimiter=",")
            dimension = log.shape
            logs.append(log)
            nFile +=1

        avgLog = np.zeros(shape=dimension)
        for log in logs:
            avgLog += log
        avgLog /= nFile
        p, beta = avgLog[-1][2]/(avgLog[-1][1] + avgLog[-1][2]), float(header[8:12])
        prevalance.append(p)
        spreadingRate.append(beta) # gamma = 1
        np.savetxt(folder +'/avg.txt', avgLog, delimiter=',')

    #2.Plot prevalance vs spreadingRate
    spreadingRate.sort()
    prevalance.sort()
    plt.plot(spreadingRate, prevalance)
    plt.ylabel('Prevalance')
    plt.xlabel('Delta')
    plt.savefig('prevalance_SF.png')


#1. Read simulation logs from folder
path = sys.argv[1]
plotPrevalance(path)



"""
nFile = 0
logs, header = [], []


for file in glob.glob(path + "*/" "/*.txt"):
    f = open(file, "rb")
    if len(header) == 0:
        header.append(f.readline())
    log = np.loadtxt(f, delimiter=",")
    logs.append(log)
    nFile +=1

#2. Average the numbers
avgLog = np.zeros(shape=log.shape)
for log in logs:
    avgLog += log
avgLog /= nFile

#3. Write the averaged log to a file
np.savetxt(path +'/avg.txt', avgLog, delimiter=',')

#4. Get timesteps, avg. # of infected, avg. # of susceptibles
time = []
avgNSusceptible = []
avgNInfected = []
for item in avgLog:
    time.append(int(item[0]))
    avgNSusceptible.append(int(item[1]))
    avgNInfected.append(int(item[2]))


#4 Plot # of infected vs time
plt.plot(time, avgNInfected)
plt.ylabel('Number of infected nodes')
plt.title(header[0])
plt.show()

#4.1 Plot prevalance vs spreadingRate
spreadingRate = [0.05, 0.1, 0.15, 0.2, 0.24, 0.25, 0.26, 0.3, 0.35, 0.4]
prevalance = [0, 0, 0, 0, 0.0018, 0.037, 0.082, 0.173, 0.265, 0.347]
plt.plot(spreadingRate, prevalance)
plt.ylabel('Prevalance')
plt.title('Threshold = 0.248')
plt.show()
"""
