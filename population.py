# ================================
# Author: Kristian N Jensen
# Date: 24/07 - 18
# Project: NEAT
# ================================

# Custom libraries
from genome import Genome
from species import Species

class Population:
    """
    Class for NEAT Algorithm 
    """

    def __init__(self, pop_size, _inSize, _outSize):
        self.pop_size = pop_size
        self.population = []
        self.species = []
        self.innovationNo = 1

        for _ in range(self.pop_size):
            gene = Genome(_inSize, _outSize)
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
            newGenes.append(s.champ.clone())
            noOfChild = int(s.avgFitness / avgSum * self.size())

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
                self.species.append(Species(gene))
    
    def sortSpecies(self):
        for s in self.species:
            s.sortSpecies()

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
