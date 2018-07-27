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
from node import Node
from connection import Connection

class Genome:
    """
    Class for a Genome in the NEAT Algorithm
    """
    def __init__(self, _in, _out, innovationHistory, clone=False):
        self.nodes = []
        self.inNodes = []
        self.outNodes = []
        self.connectedNodes = []
        self.connections = []
        self.noOutputs = _out
        self.noInputs = _in
        self.nextNode = 1
        self.maxInLayer = 10
        self.currLayer = 1
        self.currNodesInLayer = 0
        self.steps = 0
        self.fitness = 0


        for i in range(_in):
            node = Node(i+1, 'input', layer=0)
            self.nodes.append(node)
            self.inNodes.append(node)
            self.nextNode += 1

        for i in range(_out):
            node = Node(i+20, 'output', layer=20)
            self.nodes.append(node)
            self.outNodes.append(node)
            self.nextNode += 1
        
        if not clone:
            self.add_connection(innovationHistory)


    def forward(self, _input):
        """
        Move an input forward through the genome (Neural Net)
        """
        for node in self.nodes:
            node.clear()

        output = [0] * self.noOutputs
        j = 0
        for i, node in enumerate(self.nodes):
            if node.nodeType == 'input':
                node.value = _input[j]
                j += 1
            connections = node.connections
            for connection in connections:
                connection.forward()

        j = 0
        for i, node in enumerate(self.nodes):
            if node.nodeType == 'output':
                output[j] = node.value
                j += 1

        return output

    def getAction(self, _input):
        output = self.forward(_input)
        action = np.argmax(output)
        return action

    def add_connection(self, innovationHistory):
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
        if node1.nodeType == node2.nodeType:
            return True
        if node1.layer == node2.layer:
            return True
        if node1.nodeType == 'output':
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
        clone = Genome(len(self.inNodes), len(self.outNodes), innovationHistory, clone=True)
        clone.connections = deepcopy(self.connections)
        clone.connectedNodes = deepcopy(self.connectedNodes)
        clone.hiddenNodes = deepcopy(self.hiddenNodes)
        return clone
    
    def mutate(self, innovationHistory):
        """
        Mutates the genome in one of four ways
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
            self.add_connection(innovationHistory)

        r3 = random.random()
        if r3 < 0.02:
            # 2 % of the time add a new node
            self.addNode(innovationHistory)

    def __repr__(self):
        return "Genome: \n===> Nodes - {}, \n===> connections - {}".format(
            self.nodes, 
            self.connections
        ) 