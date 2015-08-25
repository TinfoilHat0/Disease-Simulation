from _NetworKit import Graph
import matplotlib.pyplot as plt
import numpy as np

class SIS:
    """ Implementation of the SIS simulation """
    def __init__(self, G, beta, gamma, n0, t):
        """
            G: Network
            beta: Infect prob.
            gamma: Cure prob.
            n0: Initial # of the infected nodes
            t: # of timesteps
        """
        self.G = G
        self.n0 = int(n0)
        self.size = G.numberOfNodes()
        if self.n0 > self.size:
            raise ValueError('Initial # of infected population must be smaller than networks size')
        self.beta = beta
        self.gamma = gamma
        self.susceptible = []
        self.infected = []
        self.toInfect = []
        self.log = []
        self.t = t

    def setup(self):
        """ Sets up initial states for the nodes of the network """
        #0. Reset node states in case of multiple simulations are run using the same class
        self.susceptible = []
        self.infected = []
        self.toInfect = []
        self.log = []
        #1. Set state of all nodes to susceptible
        for n in range(0, self.size):
            self.susceptible.append(n)
        #2. Distribute initial infections to network randomly
        count = 0
        while count < self.n0:
            r = np.random.random_integers(low=0, high=self.size-1)
            if r in self.susceptible:
                self.susceptible.remove(r)
                self.infected.append(r)
                count += 1
        self.log.append((0, self.size - self.n0, self.n0))

    def run(self, filename):
        """ Runs a SIS simulation on given network and with supplied parameters and returns the sim. log """
        #1. Set initial conditions for the network
        self.setup()
        #2. Run simulation for t timesteps
        for step in range(1, self.t+1):
            #2.1 Each infected node spreads infection to its neighbors with beta prob.
            for u in self.infected:
                for v in self.G.neighbors(u):
                    if v not in self.toInfect:
                        r = np.random.random_sample()
                        if r < self.beta:
                            self.toInfect.append(v)
            #2.2 Update state of newly infected nodes
            for v in self.toInfect:
                if v in self.susceptible:
                    self.infected.append(v)
                    self.susceptible.remove(v)
            #2.3 Cure infected nodes with gamma prob.
            for u in self.infected:
                r = np.random.random_sample()
                if r < self.gamma:
                    self.infected.remove(u)
                    self.susceptible.append(u)
            self.toInfect = []
            #2.4 Record # of susceptible and infected in log for this timestep
            nInfected = len(self.infected)
            nSusceptible = len(self.susceptible)
            self.log.append((step, nSusceptible, nInfected))
            #2.5 Print progress of simulation in every %10
            progress = (step/self.t)*100
            if progress >= 10 and progress % 10 == 0:
                print('Progress: ' + str(progress))

        self.saveResults(filename)
        return self.log

    def saveResults(self, filename):
        """ Saves result of simulation """
        file = open(filename,'w')
        file.write("# Beta: " + str(self.beta) + " Gamma: " + str(self.gamma) +"\n")
        file.write("# Timestep," + "N(S)," + "N(I)" + "\n")
        for item in self.log:
            file.write(str(item[0]) + "," + str(item[1]) + "," + str(item[2]) + "\n")
