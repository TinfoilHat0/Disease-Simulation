from _NetworKit import Graph
import random

class SIS:
    """ Implementation of the SIS simulation as defined in [Chakrabarti et al., 2008] """
    def __init__(self, G, beta, gamma, n0, t):
        """
            G: Network
            beta: Infect prob.
            gamma: Cure prob.
            n0: Initial # of the infected nodes
            t: # of timesteps
        """
        self.G = G
        self.n0 = n0
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
        #1. Set state of all nodes to susceptible
        for n in range(0, self.size):
            self.susceptible.append(n)
        #2. Distribute initial infections to network randomly
        count = 0
        while count < n0:
            r = random.randint(0, self.size-1)
            if r in self.susceptible:
                self.susceptible.remove(r)
                self.infected.append(r)
                count += 1

    def run(self):
        """ Runs a SIS simulation with on given network and with supplied parameters and returns the sim. log """
        #1. Set initial conditions for the network
        self.setup()
        nInfected = len(self.infected)
        nSusceptible = len(self.susceptible)
        self.log.append((0, nSusceptible, nInfected))
        #2. Run simulation for t timesteps
        for step in range(1, self.t+1):
            #2.1 Each infected node spreads infection to its neighbors with beta prob.
            for u in self.infected:
                for v in self.G.neighbors(u):
                    if v in self.susceptible and v not in self.toInfect:
                        r = random.random()
                        if r <= self.beta:
                            self.toInfect.append(v)
            #2.2 Update state of newly infected nodes
            for v in self.toInfect:
                self.infected.append(v)
                self.susceptible.remove(v)
            self.toInfect.clear()

            #2.3 Cure infected nodes with gamma prob.
            for u in self.infected:
                r = random.random()
                if r <= self.gamma:
                    self.infected.remove(u)
                    self.susceptible.append(u)

            #2.4 Record # of susceptible and infected in log for this timestep
            nInfected = len(self.infected)
            nSusceptible = len(self.susceptible)
            self.log.append((step, nSusceptible, nInfected))

            #2.5 Print progress of simulation in every %10
            progress = int((step/self.t)*100)
            if progress >= 10 and progress % 10 == 0:
                print('Progress: ' + str(progress))

        return self.log

    def saveResults(self, path):
        """ Saves result of simulation to a file """
