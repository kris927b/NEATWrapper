# ================================
# Author: Kristian N Jensen
# Date: 24/07 - 18
# Project: NEAT
# ================================

# Built-in Libraries
from copy import deepcopy
from random import uniform

class Species:
    """Species - Class for a species in the NEAT Algorithm
        
    The Species class contains members, and an representative. For each generation you can clear the members and create new ones, that match the representative. 
    
    Args:
        gene (Genome): The representative gene for this new species.
    """
    def __init__(self, gene):
        self.members = [gene]
        self.bestFitness = gene.fitness
        self.bestSteps = gene.steps
        self.represent = gene.clone()
        self.staleness = 0
        self.avgFitness = 0
        self.champ = gene.clone()

        self.topoCoeff = 1
        self.weightCoeff = 0.5
        self.compatibilityThreshold = 3

    def compare(self, gene):
        """compare - Compares the representative gene from the species to the given gene. 
        
        Used to check if a gene matches the species. It has to get a difference below a certain threshold.
        
        Args:
            gene (Genome): Genome to compare.
        
        Returns:
            Boolean: Whether or not the differences is above or below the threshold. 
        """

        topoDiff = self.getTopologicalDiff(gene)
        weightDiff = self.getWeightDiff(gene)
        
        compatibility = (topoDiff*self.topoCoeff) + (weightDiff * self.weightCoeff)
        return (self.compatibilityThreshold > compatibility)

    def addToSpecies(self, gene):
        """addToSpecies - Adds a specified gene to the species.
        
        Used to add a new gene to the species, after it has been approved. 
        
        Args:
            gene (Genome): Genome to add to the sepcies. 
        """

        self.members.append(gene)

    def clear(self):
        """clear - Clears out all members of the species. 
        
        Clears the list of members, but keeps the representative gene so that the list of members can be filled again. 
        """

        self.members = []

    def size(self):
        """size - Returns the number of members in the species.
        
        Returns:
            Int: The number of members in the species. 
        """

        return len(self.members)

    def sortSpecies(self):
        """sortSpecies - Sorts the members of the species according to their fitness. 
        
        Used to sort the members, and find if the species is performing better than last generation. 
        """

        self.members.sort(key=lambda x: x.fitness, reverse=True)
        
        if len(self.members) == 0:
            self.staleness = 100
            return

        champ = self.members[0].fitness

        if champ > self.bestFitness:
            self.bestFitness = champ
            self.bestSteps = self.members[0].steps
            self.represent = self.members[0].clone()
            self.champ = self.members[0].clone()
        else:
            self.staleness += 1

    def getTopologicalDiff(self, gene):
        """getTopologicalDiff - Finds the difference between the representative gene and a new gene according to the topology of the incoming gene.
        
        Used to figure out how far off the genes topology is compared to the species representative. 
        
        Args:
            gene (Genome): Gene that is being checked if it fits in this species.
        
        Returns:
            Int: The difference in topology as an integer
        """

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
        """getWeightDiff - Finds the difference between the representative gene and a new gene according to the weights in the incoming gene. 
        
        Used to figure out how far off the genes weights are compared to the species representative. 
        
        Args:
            gene (Genome): Gene that is being checked if it fits in this species. 
        
        Returns:
            Int: The difference as an integer. 
        """

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
        """cull - Kills of half of the members of the species. 
        
        Used in Natural selection to kill of the worst performing half of the species. 
        """

        if self.size() > 2:
            self.members = self.members[:int(self.size()/2)]

    def shareFitness(self):
        """shareFitness - Divides all members' fitness by the number of genes in the species. 

        The function is used to "normalize" the fitness of all members of the species. 
        """

        for gene in self.members:
            gene.fitness /= self.size()

    def getAvgFitness(self):
        """getAvgFitness - Calculates the average fitness of th species. 

        Used in the process of finding the species with the highest average fitness.
        """

        _sum = 0
        for gene in self.members:
            _sum += gene.fitness

        self.avgFitness = _sum/self.size()

    def selectGene(self):
        """selectGene - Selects a gene at random, with a slight bias of the fitness. 
        
        Samples a random number between 0 and the total fitness of the current species. In a loop, it then sums up the fitness values of the members, until this sum is greater than the random number sampled. It then returns the currently selected member. 
        
        Returns:
            Genome: Genome from the species
        """

        if self.size() == 1:
            return self.members[0]

        totalFitness = 0
        for member in self.members:
            totalFitness += member.fitness

        r = uniform(0, totalFitness)
        _sum = 0
        for member in self.members:
            _sum += member.fitness
            if _sum >= r:
                return member

        return self.members[0]


    def reproduce(self, innovation):
        """reproduce - Creates a new child through crossover, and then mutates it in one of three ways
        
        This function performs crossover between two randomly selected parents. And in the end it mutates the child, that is returned from doing crossover. 
        
        Args:
            innovation (Innovation): An Innovation object, with the current innotation information for the population. 
        
        Returns:
            Genome: Returns a new genome
        """

        # STEP 1: Crossover
        parent1 = self.selectGene().clone()
        parent2 = self.selectGene().clone()

        if parent1.fitness >= parent2.fitness:
            child = parent1.crossOver(parent2)
        else:
            child = parent2.crossOver(parent1)
        
        # STEP 2: Mutation
        child.mutate(innovation)

        return child