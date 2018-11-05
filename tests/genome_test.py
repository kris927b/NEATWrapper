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

@pytest.fixture
def gene2(innovation):
    return NEATWrapper.Genome(2, 2, innovation)

def test_init(gene):
    assert gene.inNodes == 2
    assert gene.outNodes == 2
    assert len(gene.nodes) == 4
    assert len(gene.connections) == 1
    assert len(gene.connectedNodes) == 1
    assert len(gene.network) == len(gene.nodes)
    assert gene.nextNode == 5
    assert gene.currLayer == 2
    assert gene.steps == 0 and gene.fitness == 0

def test_forward(gene):
    gene.connections[0].weight = 1
    out = gene.forward([2, 2])
    assert type(out) is list
    assert len(out) == 2
    assert out[0] == 2 or out[1] == 2

def test_connectNodes(gene):
    [node.clear() for node in gene.nodes]
    assert not gene.connections[0].inNode.connections
    gene.connectNodes()
    assert len(gene.connections[0].inNode.connections) == 1

def test_generateNet(gene):
    gene.network = []
    gene.generateNet()
    layer = 0
    for node in gene.network:
        assert node.getLayer() >= layer
        layer = node.getLayer()

def test_getAction(gene):
    act = gene.getAction([2, 2])
    assert type(act) == int
    assert act == 0 or act == 1

def test_fullyConnected(gene, innovation):
    assert not gene.fullyConnected()
    for _ in range(3):
        gene.addConnection(innovation)
    assert gene.fullyConnected()
    assert innovation.innoNo == 5

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
    assert gene.currLayer == 3

def test_crossOver(gene, gene2, innovation):
    gene.addConnection(innovation)
    gene.addNode(innovation)
    child = gene.crossOver(gene2)
    assert len(child.connections) >= 3
    assert len(child.nodes) == len(gene.nodes)
    assert len(child.nodes) != len(gene2.nodes)

def test_getNode(gene):
    node = gene.getNode(3)
    assert isinstance(node, NEATWrapper.Node)
    assert node.nodeType == 'output'
    assert node.nodeId == 3

def test_searchConnection(gene, gene2):
    gene2.connections.append(
        gene.connections[0].clone(gene.connections[0].enabled)
    )
    conn = gene.searchConnection(
        gene2.connections, 
        gene.connections[0].innovation
    )
    assert isinstance(conn, NEATWrapper.Connection)
    conn = gene.searchConnection(
        gene2.connections, 
        10
    )
    assert not conn

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
    assert gene_clone.currLayer == gene.currLayer
