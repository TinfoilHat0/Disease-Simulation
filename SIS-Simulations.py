# -*- coding: utf-8 -*-
# <nbformat>3.0</nbformat>

# <codecell>

import networkit as nt
import os, sys
import SIS

# <codecell>

#0. Parse arguments
fileFormat = sys.argv[1]
file = sys.argv[2]
t = int(sys.argv[3])
curingRate = int(sys.argv[4])
initialFractionOfInfected = float(sys.argv[5])
saveFolder = sys.argv[6]

#1. Load the network and calculate the ep. threshold
#Currently, script only supports METIS and SNAP formats
if fileFormat == 'METIS':
    fileFormat = nt.Format.METIS
else:
    fileFormat = nt.Format.SNAP
G = nt.readGraph(file, fileFormat)
epThreshold = 1/(nt.algebraic.adjacencyEigenvector(G, 0)[0])

# <codecell>

#2. Get network properties
#Number of nodes, Max deg., avg. deg, clustering.coeff, modularity, power law gamma
N = G.numberOfNodes()
dmax = nt.properties.GraphProperties.minMaxDegree(G)[1]
k = nt.properties.GraphProperties.averageDegree(G)
ck = nt.properties.GraphProperties.averageLocalClusteringCoefficient(G)
zeta = nt.community.detectCommunities(G)
mod = nt.community.Modularity().getQuality(zeta, G)
isPowerLaw, gamma = nt.properties.degreePowerLaw(G), 0
if isPowerLaw[0] == True:
    gamma = isPowerLaw[2]

# <codecell>

#3. Simulation parameters
fractions, betas = [10, 5, 3, 2, 1,  1/2, 1/3, 1/4, 1/5, 1/6], []
for fraction in fractions:
    betas.append(round(epThreshold/fraction, 4))
n0 = N*initialFractionOfInfected


# <codecell>

#4. Run simulation
parentFolder = saveFolder
if not os.path.exists(parentFolder):
        os.makedirs(parentFolder)
#4.1. Record parameters
f = open(parentFolder + 'parameters', 'w')
f.write('# of nodes: ' + str(N) +'\n')
f.write('Max.Degree: ' + str(dmax) + '\n')
f.write('Clustering Coeff: ' + str(ck) + '\n')
f.write('Modularity: ' + str(mod) + '\n')
f.write('Gamma: ' + str(gamma) + '\n')
f.write('Ep. Threshold: ' + str(epThreshold) + '\n')
f.write('# of steps: ' + str(t) + '\n')
f.write('Curing rate: ' + str(curingRate) + '\n')
f.close()

#4.2. Record result of runs
for beta in betas:
    folderName = parentFolder + str(beta) +'/'
    if not os.path.exists(folderName):
        os.makedirs(folderName)
    sim = SIS.SIS(G, beta, curingRate, n0, t)
    for i in range(0, 5):
        fileName = folderName + 'run' + str(i) + '.txt'
        sim.run(fileName)
# <codecell>
