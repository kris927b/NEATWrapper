# ================================
# Author: Kristian N Jensen
# Date: 24/07 - 18
# Project: NEAT
# ================================

# Built-in Libraries
from copy import deepcopy
from random import uniform

class Species:
    """
    Class for a species in the NEAT Algorithm
    """
    def __init__(self, gene, innovation):
        self.members = [gene]
        self.bestFitness = gene.fitness
        self.bestSteps = gene.steps
        self.represent = gene.clone(innovation)
        self.staleness = 0
        self.avgFitness = 0
        self.champ = gene.clone(innovation)

        self.topoCoeff = 1
        self.weightCoeff = 0.5
        self.compatibilityThreshold = 3

    def compare(self, gene):
        topoDiff = self.getTopologicalDiff(gene)
        weightDiff = self.getWeightDiff(gene)
        
        compatibility = (topoDiff*self.topoCoeff) + (weightDiff * self.weightCoeff)
        return (self.compatibilityThreshold > compatibility)

    def addToSpecies(self, gene):
        self.members.append(gene)

    def clear(self):
        self.members = []

    def size(self):
        return len(self.members)

    def sortSpecies(self, innovation):
        self.members.sort(key=lambda x: x.fitness, reverse=True)
        
        if len(self.members) == 0:
            self.staleness = 100
            return

        champ = self.members[0].fitness

        if champ > self.bestFitness:
            self.bestFitness = champ
            self.bestSteps = self.members[0].steps
            self.represent = self.members[0].clone(innovation)
            self.champ = self.members[0].clone(innovation)
        else:
            self.staleness += 1

    def getTopologicalDiff(self, gene):
        connect1 = self.represent.connections
        connect2 = gene.connections
        match = 0
        for i in range(len(connect1)):
            for j in range(len(connect2)):
                if connect1[i].innovation == connect2[j].innovation:
                    match += 1
                    break

        return (len(connect1) + len(connect2) - (2*match))

    def getWeightDiff(self, gene):
        connect1 = self.represent.connections
        connect2 = gene.connections
        match = 0
        totalDiff = 0
        for i in range(len(connect1)):
            for j in range(len(connect2)):
                if connect1[i].innovation == connect2[j].innovation:
                    match += 1
                    totalDiff += abs(connect1[i].weight - connect2[j].weight)
                    break

        if match == 0:
            return 100

        return totalDiff/match

    def cull(self):
        if self.size() > 2:
            self.members = self.members[:int(self.size()/2)]

    def shareFitness(self):
        for gene in self.members:
            gene.fitness /= self.size()

    def getAvgFitness(self):
        _sum = 0
        for gene in self.members:
            _sum += gene.fitness

        self.avgFitness = _sum/self.size()

    def selectGene(self):
        # * If only one member, then return that one
        if self.size() == 1:
            return self.members[0]

        # * Find the total fitness between all genes in the species
        totalFitness = 0
        for member in self.members:
            totalFitness += member.fitness

        # * Sample a random number between 0 and the total fitness
        r = uniform(0, totalFitness)

        # * Sum all the fitness values up once again, but this time return the gene that flips the sum over the random number sampled above.
        _sum = 0
        for member in self.members:
            _sum += member.fitness
            if _sum >= r:
                return member

        # * For security we return the best gene in the species if the above algorithm yielded no result.
        return self.members[0]


    def reproduce(self, innovationHistory):
        # NotImplementedError("Remember to implement reproduction")
        """
        Creates a new child through crossover, and then mutates it in one of four ways
        """
        # TODO: STEP 1: Crossover


        # STEP 2: Mutation
        child = self.selectGene().clone(innovationHistory)

        child.mutate(innovationHistory)

        return child