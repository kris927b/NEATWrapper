# ================================
# Author: Kristian N Jensen
# Date: 24/07 - 18
# Project: NEAT
# ================================

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

        for _ in range(self.pop_size):
            gene = Genome(_inSize, _outSize, self.innovationHistory)
            self.population.append(gene)

    def getGene(self, i):
        return self.population[i]

    def size(self):
        return len(self.population)

    def naturalSelection(self):
        self.calcFitness()
        self.speciate()
        self.sortSpecies()
        self.cullSpecies()

        newGenes = []
        avgSum = self.getAvgFitnessSum()
        for s in self.species:
            newGenes.append(s.champ.clone(self.innovationHistory))
            noOfChild = int(s.avgFitness / avgSum * self.size()) - 1
            for _ in range(noOfChild):
                newGenes.append(s.reproduce(self.innovationHistory))

        while len(newGenes) < self.pop_size:
            newGenes.append(self.species[0].reproduce(self.innovationHistory))

        self.population = []
        self.population = newGenes

    def calcFitness(self):
        sums = 0
        for gene in self.population:
            sums += pow(gene.steps, 2)
        
        for gene in self.population:
            gene.fitness = gene.steps / sums
        
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
                self.species.append(Species(gene, self.innovationHistory))
    
    def sortSpecies(self):
        # * Check how many members each species have
        self.species = [s for s in self.species if len(s.members) > 0]

        # * Sort each species individually
        for s in self.species:
            s.sortSpecies(self.innovationHistory)

        # * Sort the entire list of species according to the champion in each species
        self.species.sort(key=lambda x: x.bestFitness, reverse=True)

    def cullSpecies(self):
        for s in self.species:
            s.cull()
            s.shareFitness()
            s.getAvgFitness()

    def getAvgFitnessSum(self):
        _sum = 0
        for s in self.species:
            _sum += s.avgFitness

        return _sum


if __name__ == '__main__':
    neat = Population(1, 2, 2)
