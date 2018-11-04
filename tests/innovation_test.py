# ================================
# Author: Kristian N Jensen
# Date: 03/11 - 18
# Project: NEAT
# ================================

# * Third-party libraries
import pytest
import sys

sys.path.append('../')

# * Custom Libraries 
import NEATWrapper

@pytest.fixture
def innovation():
    return NEATWrapper.Innovation()

@pytest.fixture
def node1():
    return NEATWrapper.Node(1, 'input', layer=1)

@pytest.fixture
def node2():
    return NEATWrapper.Node(2, 'output', layer=2)

@pytest.fixture
def node3():
    return NEATWrapper.Node(3, 'output', layer=2)

def test_init(innovation):
    assert not innovation.connectionsDone
    assert innovation.innoNo == 1

def test_checkConnection(innovation, node1, node2, node3):
    conn1 = innovation.checkConnection(node1, node2)
    assert conn1.innovation == 1
    assert len(innovation.connectionsDone) == 1
    conn2 = innovation.checkConnection(node1, node2)
    assert conn2.innovation == 1
    assert len(innovation.connectionsDone) == 1
    conn3 = innovation.checkConnection(node1, node3)
    assert conn3.innovation == 2
    assert len(innovation.connectionsDone) == 2
