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
    def __init__(self, _in, _out, clone=False):
        self.nodes = []
        self.connectedNodes = []
        self.connections = []
        self.noOutputs = _out
        self.steps = 0
        self.fitness = 0

        for i in range(_in):
            node = Node(i+1, 'input')
            self.nodes.append(node)

        for i in range(_out):
            node = Node(i+20, 'output')
            self.nodes.append(node)
        
        if not clone:
            self.add_connection(1)


    def forward(self, _input):
        """
        Move an input forward through the genome (Neural Net)
        """
        for node in self.nodes:
            node.clear()

        output = [0] * self.noOutputs
        for i, node in enumerate(self.nodes):
            if node.nodeType == 'input':
                node.value = _input[i]
            connections = node.connections
            for connection in connections:
                connection.forward()

        for i, node in enumerate(self.nodes):
            if node.nodeType == 'output':
                output[i] = node.value

        return output

    def getAction(self, _input):
        output = self.forward(_input)
        action = np.argmax(output)
        return action

    def add_connection(self, innovation):
        """
        Add a connection to the genome
        """
        inNode = random.randint(0, len(self.inNodes)-1)
        outNode = random.randint(0, len(self.outNodes)-1)
        connect = (inNode, outNode)
        if connect in self.connectedNodes:
            return

        connection = Connection(self.inNodes[inNode],
            self.outNodes[outNode],
            weight=random.randint(-2, 2),
            innovation=innovation
        )
        self.inNodes[inNode].connection = connection
        self.inNodes[inNode].isConnected = True
        self.connectedNodes.append(connect)
        self.connections.append(connection)
    
    def clear(self):
        self.steps = 0
        self.fitness = 0

    def clone(self):
        clone = Genome(len(self.inNodes), len(self.outNodes), clone=True)
        clone.connections = deepcopy(self.connections)
        clone.connectedNodes = deepcopy(self.connectedNodes)
        clone.hiddenNodes = deepcopy(self.hiddenNodes)
        return clone


    def __repr__(self):
        return "Genome: \n===> inNodes - {}, \n===> outNodes - {}, \n===> connections - {}".format(
            self.inNodes, 
            self.outNodes, 
            self.connections
        ) 