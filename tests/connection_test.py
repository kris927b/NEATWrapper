# ================================
# Author: Kristian N Jensen
# Date: 23/10 - 18
# Project: NEAT
# ================================

# * Third-party libraries
import pytest
import sys

sys.path.append('../')

# * Custom Libraries 
import NEATWrapper

@pytest.fixture
def connection():
    _in = NEATWrapper.Node(1, 'input', layer=1)
    _out = NEATWrapper.Node(2, 'out', layer=2)
    weight = 2
    return NEATWrapper.Connection(_in, _out, weight)


def test_standard_init(connection):
    assert connection.weight == 2
    assert connection.innovation == 0

def test_getInnovationNo(connection):
    assert connection.getInnovationNo() == 0

def test_setInnovationNo(connection):
    connection.setInnovationNo(1)
    assert connection.innovation == 1

def test_mutateWeights(connection):
    w = connection.weight
    connection.mutateWeights()
    assert w != connection.weight

def test_forward(connection):
    connection.inNode.value = 10
    connection.forward()
    assert connection.outNode.value == 20