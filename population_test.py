# ================================
# Author: Kristian N Jensen
# Date: 24/07 - 18
# Project: NEAT
# ================================

# Custom libraries
from population import Population

def test_population():
    pop = Population(2, 2, 2)
    assert len(pop.population) == 2