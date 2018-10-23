# ================================
# Author: Kristian N Jensen
# Date: 12/10 - 18
# Project: NEAT
# ================================

# Custom libraries
from NEATWrapper import Population
from NEATWrapper import Genome

# ThirdParty Libraries
import pytest

@pytest.fixture
def pop():
    return Population(2, 2, 2)

def test_population(pop):
    assert len(pop.population) == 2

def test_pop_size(pop):
    assert pop.size() == 2

def test_get_gene(pop):
    gene = pop.getGene(0)
    assert type(gene) is Genome