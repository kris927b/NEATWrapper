# ================================
# Author: Kristian N Jensen
# Date: 12/10 - 18
# Project: NEAT
# ================================

# ThirdParty Libraries
import pytest
import sys
from math import inf

sys.path.append('../')

# Custom libraries
import NEATWrapper

@pytest.fixture
def pop():
    return NEATWrapper.Population(4, 2, 2)

def test_init(pop):
    assert len(pop.population) == 4
    assert isinstance(pop.population[0], NEATWrapper.Genome)
    assert len(pop.species) == 0
    assert isinstance(pop.innovationHistory, NEATWrapper.Innovation)
    assert pop.pop_size == 4
    assert not pop.bestGene
    assert pop.bestScore == -inf

def test_size(pop):
    assert pop.size() == 4

def test_getGene(pop):
    gene = pop.getGene(0)
    assert isinstance(gene, NEATWrapper.Genome)
    assert gene == pop.population[0]

def test_findBestGene(pop):
    for i, gene in enumerate(pop.population):
        gene.steps = i+1
    pop.calcFitness()
    pop.speciate()
    pop.sortSpecies()
    pop.findBestGene()
    assert isinstance(pop.bestGene, NEATWrapper.Genome)
    assert pop.bestScore != -inf

def test_getBestGene(pop):
    gene = pop.getBestGene()
    assert not gene
    for i, gene in enumerate(pop.population):
        gene.steps = i+1
    pop.calcFitness()
    pop.speciate()
    pop.sortSpecies()
    pop.findBestGene()
    gene = pop.getBestGene()
    assert isinstance(gene, NEATWrapper.Genome)

def test_getBestScore(pop):
    score = pop.getBestScore()
    assert score == -inf
    for i, gene in enumerate(pop.population):
        gene.steps = i+1
    pop.calcFitness()
    pop.speciate()
    pop.sortSpecies()
    pop.findBestGene()
    score = pop.getBestScore()
    assert isinstance(score, int)
    assert score == 4

def test_calcFitness(pop):
    for i in range(pop.size()):
        gene = pop.getGene(i)
        gene.steps = 10

    pop.calcFitness()

    for i in range(pop.size()):
        gene = pop.getGene(i)
        assert gene.fitness == (10/400)

def test_speciate(pop):
    assert len(pop.species) == 0
    pop.speciate()
    assert len(pop.species) > 0

def test_killStaleSpecies(pop):
    pop.speciate()
    pop.killStaleSpecies()
    assert len(pop.species) > 0

    for s in pop.species:
        s.staleness = 15

    pop.killStaleSpecies()
    assert len(pop.species) == 0

def test_sortSpecies(pop):
    pop.speciate()
    pop.sortSpecies()
    assert pop.species[0].bestFitness >= pop.species[-1].bestFitness

def test_cullSpecies(pop):
    pop.speciate()
    noMembers = [len(s.members) for s in pop.species]

    for i in range(pop.size()):
        gene = pop.getGene(i)
        gene.steps = 10
    pop.calcFitness()
    pop.cullSpecies()

    # * Testing that the cull function does it job correctly.
    for i, s in enumerate(pop.species):
        assert (len(s.members) <= 2) or (len(s.members) == int(noMembers[i]/2))

    # * Testing that the shareFitness function performs it job in this context.
    for i in range(pop.size()):
        gene = pop.getGene(i)
        assert gene.fitness <= (10/400)

    # * Testing that the getAvgFitness function performs it job in this context
    for s in pop.species:
        assert s.avgFitness > 0

def test_getAvgFitnessSum(pop):
    pop.speciate()
    for i in range(pop.size()):
        gene = pop.getGene(i)
        gene.steps = 10
    pop.calcFitness()
    pop.cullSpecies()
    [s.getAvgFitness() for s in pop.species if s.size() > 0]
    _sum = sum([s.avgFitness for s in pop.species])
    avgfit = pop.getAvgFitnessSum()*len(pop.species)
    assert isinstance(avgfit, float)
    assert avgfit == _sum

