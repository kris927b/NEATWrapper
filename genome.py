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
        self.steps = 0
        self.fitness = 0

        for i in range(_in):
            node = Node(i+1, 'input', layer=0)
            self.nodes.append(node)
            self.inNodes.append(node)

        for i in range(_out):
            node = Node(i+20, 'output', layer=20)
            self.nodes.append(node)
            self.outNodes.append(node)
        
        if not clone:
            self.add_connection(innovationHistory)
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

    def clear(self):
        self.steps = 0
        self.fitness = 0

    def clone(self, innovationHistory):
        clone = Genome(len(self.inNodes), len(self.outNodes), innovationHistory, clone=True)
        clone.connections = deepcopy(self.connections)
        clone.connectedNodes = deepcopy(self.connectedNodes)
        clone.hiddenNodes = deepcopy(self.hiddenNodes)
        return clone


    def __repr__(self):
        return "Genome: \n===> Nodes - {}, \n===> connections - {}".format(
            self.nodes, 
            self.connections
        ) 