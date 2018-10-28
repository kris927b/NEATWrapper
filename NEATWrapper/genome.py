# ================================
# Author: Kristian N Jensen
# Date: 24/07 - 18
# Project: NEAT
# ================================

# Built-in libraries
import random
from copy import deepcopy

# Third-party libraries
import numpy as np

# Custom libraries
from NEATWrapper.node import Node
from NEATWrapper.connection import Connection

class Genome:
    """
    Class for a Genome in the NEAT Algorithm
    @param _in: Number of input nodes \n
    @param _out: Number of output nodes \n
    @param innovationHistory: innovationHistory class for all the genes in the population. Described in the innovation.py file.
    @param clone: bool whether or not the gene is a clone of a previous created gene.
    """
    def __init__(self, _in, _out, innovationHistory, clone=False):
        self.nodes = []
        self.inNodes = _in
        self.outNodes = _out
        self.connectedNodes = []
        self.connections = []
        self.network = []
        self.nextNode = 1
        self.maxInLayer = 10
        self.currLayer = 1
        self.currNodesInLayer = 0
        self.steps = 0
        self.fitness = 0

        if not clone:
            for i in range(_in):
                node = Node(i+1, 'input', layer=0)
                self.nodes.append(node)
                self.nextNode += 1

            for i in range(_out):
                node = Node(i+20, 'output', layer=20)
                self.nodes.append(node)
                self.nextNode += 1
        
            self.addConnection(innovationHistory)


    def forward(self, _input):
        """
        Move an input forward through the genome (Neural Net)
        """
        for node in self.nodes:
            node.reset()

        output = [0] * self.outNodes
        j = 0
        for i in range(self.inNodes):
            self.nodes[i].setValue(_input[i])

        for i in range(len(self.network)):
            self.network[i].forward()

        for i in range(self.outNodes):
            output[i] = self.nodes[self.inNodes + i].value

        return output

    def connectNodes(self):
        for node in self.nodes:
            node.clear()

        for connection in self.connections:
            connection.inNode.addConnection(connection)

    def generateNet(self):
        self.connectNodes()
        self.network = []

        for i in range(self.currLayer):
            for j in range(len(self.nodes)):
                if self.nodes[j].getLayer() == i:
                    self.network.append(self.nodes[j])

    def getAction(self, _input):
        output = self.forward(_input)
        action = int(np.argmax(output))
        return action

    def addConnection(self, innovationHistory):
        """
        Add a connection to the genome
        """
        inNode = random.randint(0, len(self.nodes)-1)
        outNode = random.randint(0, len(self.nodes)-1)
        connect = (inNode, outNode)
        
        node1 = self.nodes[inNode]
        node2 = self.nodes[outNode]

        while self.nodesAreSimilar(node1, node2) or connect in self.connectedNodes:
            inNode = random.randint(0, len(self.nodes)-1)
            outNode = random.randint(0, len(self.nodes)-1)
            connect = (inNode, outNode)
            node1 = self.nodes[inNode]
            node2 = self.nodes[outNode]

        connection = innovationHistory.checkConnection(node1, node2)

        self.nodes[inNode].connection = connection
        self.nodes[inNode].isConnected = True
        self.connectedNodes.append(connect)
        self.connections.append(connection)

    def nodesAreSimilar(self, node1, node2):
        if node1.nodeId == node2.nodeId:
            return True
        if node1.nodeType == 'output':
            return True
        if node2.nodeType == 'input':
            return True
        if node1.layer == node2.layer:
            return True

        return False

    def addNode(self, innovationHistory):
        """
        Create a new node in the genome
        """
        randomConnection = random.randint(0, len(self.connections)-1)
        connect = self.connections[randomConnection]
        connect.enabled = False

        newNodeNo = self.nextNode
        newNode = Node(newNodeNo, 'hidden', layer = self.currLayer)
        self.nodes.append(newNode)

        newConnection1 = innovationHistory.checkConnection(newNode, connect.outNode, weight=connect.weight)
        self.connections.append(newConnection1)
        self.connectedNodes.append((len(self.nodes)-1, self.nodes.index(connect.outNode)))

        newConnection2 = innovationHistory.checkConnection(connect.inNode, newNode, weight=1)
        self.connections.append(newConnection2)
        self.connectedNodes.append((self.nodes.index(connect.inNode), len(self.nodes)-1))

        self.nextNode += 1
        self.currNodesInLayer += 1
        if self.currNodesInLayer == self.maxInLayer:
            self.currLayer += 1
            self.currNodesInLayer = 0

    def clear(self):
        self.steps = 0
        self.fitness = 0

    def clone(self, innovationHistory):
        clone = Genome(self.inNodes, self.outNodes, innovationHistory, clone=True)
        clone.connections = deepcopy(self.connections)
        clone.connectedNodes = deepcopy(self.connectedNodes)
        clone.nodes = deepcopy(self.nodes)
        clone.nextNode = deepcopy(self.nextNode)
        clone.currNodesInLayer = deepcopy(self.currNodesInLayer)
        clone.currLayer = deepcopy(self.currLayer)
        return clone
    
    def mutate(self, innovationHistory):
        """
        Mutates the genome in one of three ways
        1) Weight mutation
        2) Add random connection
        3) Add new node
        """

        r = random.random()
        if r < 0.8:
            # 80 % of the time do weight mutation
            for connection in self.connections:
                connection.mutateWeights()

        r2 = random.random()
        if r2 < 0.05:
            # 5 % of the time add a connection
            self.addConnection(innovationHistory)

        r3 = random.random()
        if r3 < 0.02:
            # 2 % of the time add a new node
            self.addNode(innovationHistory)

    def __repr__(self):
        return "Genome: \n===> Nodes - {}, \n===> connections - {}".format(
            self.nodes, 
            self.connections
        ) 