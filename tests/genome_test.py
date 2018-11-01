# ================================
# Author: Kristian N Jensen
# Date: 24/10 - 18
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
def gene(innovation):
    return NEATWrapper.Genome(2, 2, innovation)

def test_geneInit(gene):
    assert gene.inNodes == 2
    assert gene.outNodes == 2
    assert len(gene.nodes) == 4
    assert len(gene.connections) == 1
    assert len(gene.connectedNodes) == 1

def test_forward(gene):
    out = gene.forward([2, 2])
    assert type(out) is list
    assert len(out) == 2

def test_getAction(gene):
    act = gene.getAction([2, 2])
    assert type(act) == int

def test_addConnection(gene, innovation):
    gene.addConnection(innovation)
    assert len(gene.connections) == 2

def test_nodesAreSimilar(gene):
    node1 = gene.nodes[0]
    node2 = gene.nodes[1]
    # * Testing for nodes in same layer and node 2 being an input node
    assert gene.nodesAreSimilar(node1, node2)
    # * Testing a good pair of nodes
    node2 = gene.nodes[2]
    assert not gene.nodesAreSimilar(node1, node2)
    # * Testing for node 1 being output node
    node1 = gene.nodes[3]
    assert gene.nodesAreSimilar(node1, node2)

def test_addNode(gene, innovation):
    gene.addNode(innovation)
    assert len(gene.nodes) == 5
    assert len(gene.connections) == 3
    assert len(gene.connectedNodes) == 3
    assert gene.nextNode == 6
    assert gene.currNodesInLayer == 1
    assert gene.currLayer == 1

def test_clear(gene):
    gene.steps = 10
    gene.fitness = 0.1
    assert gene.steps == 10
    assert gene.fitness == 0.1
    gene.clear()
    assert gene.steps == 0
    assert gene.fitness == 0

def test_clone(gene, innovation):
    gene.addNode(innovation)
    gene_clone = gene.clone()
    assert gene_clone is not gene
    assert len(gene_clone.connections) == len(gene.connections)
    assert len(gene_clone.nodes) == len(gene.nodes)
    assert len(gene_clone.connectedNodes) == len(gene.connectedNodes)
    assert gene_clone.nextNode == gene.nextNode
    assert gene_clone.currNodesInLayer == gene.currNodesInLayer
    assert gene_clone.currLayer == gene.currLayer
