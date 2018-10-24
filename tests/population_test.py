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
    return NEATWrapper.Population(2, 2, 2)

def test_population_init(pop):
    assert len(pop.population) == 2

def test_pop_size(pop):
    assert pop.size() == 2

def test_get_gene(pop):
    gene = pop.getGene(0)
    assert type(gene) is NEATWrapper.Genome

def test_calc_fitness(pop):
    for i in range(pop.size()):
        gene = pop.getGene(i)
        gene.steps = 10

    pop.calcFitness()

    for i in range(pop.size()):
        gene = pop.getGene(i)
        gene.fitness = 0.05