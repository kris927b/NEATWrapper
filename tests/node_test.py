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
def node():
    n = NEATWrapper.Node(1, 'input', layer=1)
    return n

@pytest.fixture
def output_node():
    n = NEATWrapper.Node(2, 'output', layer=2)
    return n

@pytest.fixture
def conn(node, output_node):
    conn = NEATWrapper.Connection(node, output_node, 1)
    return conn

def test_init(node):
    assert node.nodeId == 1
    assert node.nodeType == 'input'
    assert node.isConnected == False
    assert not node.connections
    assert node.value == 0
    assert node.layer == 1

def test_setValue(node):
    node.setValue(10)
    assert node.value == 10

def test_reset(node):
    node.setValue(10)
    assert node.value == 10
    node.reset()
    assert node.value == 0

def test_addConnection(node, output_node, conn):
    node.addConnection(conn)
    assert len(node.connections) == 1
    assert node.connections[0] == conn

def test_clear(node, output_node, conn):
    node.addConnection(conn)
    assert len(node.connections) == 1
    node.clear()
    assert not node.connections

def test_getLayer(node, output_node):
    assert node.getLayer() == 1
    assert output_node.getLayer() == 2

def test_clone(node, conn):
    node.addConnection(conn)
    clone = node.clone()
    assert clone.nodeId == node.nodeId
    assert clone.nodeType == node.nodeType
    assert clone.layer == node.layer
    assert len(clone.connections) == len(node.connections)
    assert clone.isConnected == node.isConnected

def test_forward(node, conn):
    node.addConnection(conn)
    node.setValue(10)
    node.forward()
    assert conn.outNode.value == 10