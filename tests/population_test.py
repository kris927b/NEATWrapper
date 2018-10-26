# ================================
# Author: Kristian N Jensen
# Date: 12/10 - 18
# Project: NEAT
# ================================

# ThirdParty Libraries
import pytest
import sys

sys.path.append('../')

# Custom libraries
import NEATWrapper

@pytest.fixture
def pop():
    return NEATWrapper.Population(4, 2, 2)

def test_populationInit(pop):
    assert len(pop.population) == 4
    assert len(pop.species) == 0
    assert type(pop.innovationHistory) is NEATWrapper.Innovation

def test_size(pop):
    assert pop.size() == 4

def test_getGene(pop):
    gene = pop.getGene(0)
    assert type(gene) is NEATWrapper.Genome

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

def test_sortSpecies(pop):
    pop.speciate()
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