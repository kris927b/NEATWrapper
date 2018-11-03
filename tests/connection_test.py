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


def test_init(connection):
    assert isinstance(connection.inNode, NEATWrapper.Node)
    assert isinstance(connection.outNode, NEATWrapper.Node)
    assert connection.weight == 2
    assert connection.innovation == 0
    assert connection.enabled == True

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

def test_sigmoid(connection):
    assert connection.sigmoid(0) == 0.5

def test_relu(connection):
    assert connection.relu(10) == 10
    assert connection.relu(-10) == 0

def test_clone(connection):
    clone = connection.clone(connection.enabled)
    assert clone.inNode == connection.inNode
    assert clone.outNode == connection.outNode
    assert clone.weight == connection.weight
    assert clone.enabled == connection.enabled
    assert clone.innovation == connection.innovation