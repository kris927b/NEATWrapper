# ================================
# Author: Kristian N Jensen
# Date: 24/07 - 18
# Project: NEAT
# ================================

# Built-in libraries
from math import inf

# Custom libraries
from NEATWrapper.genome import Genome
from NEATWrapper.species import Species
from NEATWrapper.innovation import Innovation

class Population:
    """
    Class for NEAT Algorithm 
    """

    def __init__(self, pop_size, _inSize, _outSize):
        self.pop_size = pop_size
        self.population = []
        self.species = []
        self.innovationHistory = Innovation()
        self.bestScore = -inf
        self.bestGene = None

        for _ in range(self.pop_size):
            gene = Genome(_inSize, _outSize, self.innovationHistory)
            self.population.append(gene)

    def getGene(self, i):
        return self.population[i]

    def size(self):
        return self.pop_size

    def naturalSelection(self):
        self.calcFitness()
        self.speciate()
        self.sortSpecies()
        self.cullSpecies()
        self.findBestGene()
        self.killStaleSpecies()
        self.killBadSpecies()

        self.population = []
        avgSum = self.getAvgFitnessSum()
        for s in self.species:
            self.population.append(s.champ.clone())
            noOfChild = int(s.avgFitness / avgSum * self.size()) - 1
            for _ in range(noOfChild):
                self.population.append(s.reproduce(self.innovationHistory))

        while len(self.population) < self.size():
            self.population.append(self.species[0].reproduce(self.innovationHistory))

        for gene in self.population:
            gene.generateNet()

        print(f'Number of innovations: {self.innovationHistory.size()}')

    def findBestGene(self):
        gensBestGene = self.species[0].members[0]
        gensBestScore = gensBestGene.steps

        if gensBestScore > self.bestScore:
            self.bestScore = gensBestScore
            self.bestGene = gensBestGene
    
    def killBadSpecies(self):
        avgSum = self.getAvgFitnessSum()
        self.species[:] = [s for s in self.species if int(s.avgFitness / avgSum * self.pop_size) >= 1 and len(s.members) > 0]

    def getBestGene(self):
        return self.bestGene

    def getBestScore(self):
        return self.bestScore

    def calcFitness(self):
        sums = sum([gene.steps for gene in self.population])
        
        for gene in self.population:
            gene.fitness = gene.steps**2 / sums
        
    def speciate(self):
        for s in self.species:
            s.clear()
        
        for gene in self.population:
            gotSpecies = False
            for s in self.species:
                if s.compare(gene):
                    s.addToSpecies(gene)
                    gotSpecies = True
                    break
            if not gotSpecies:
                self.species.append(Species(gene))

    def killStaleSpecies(self):
        self.species[:] = [s for s in self.species if s.staleness < 15]
    
    def sortSpecies(self):
        # * Sort each species individually
        for s in self.species:
            s.sortSpecies()

        # * Sort the entire list of species according to the champion in each species
        self.species.sort(key=lambda x: x.bestFitness, reverse=True)

    def cullSpecies(self):
        for s in self.species:
            if s.size() > 0:
                s.cull()
                s.shareFitness()
                s.getAvgFitness()

    def getAvgFitnessSum(self):
        _sum = sum([s.avgFitness for s in self.species])

        return _sum

    def clearBest(self):
        self.bestGene = None
        self.bestScore = -inf

if __name__ == '__main__':
    neat = Population(1, 2, 2)
