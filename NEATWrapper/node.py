# ================================
# Author: Kristian N Jensen
# Date: 24/07 - 18
# Project: NEAT
# ================================

from copy import deepcopy

class Node:
    """
    Class for a Node in the NEAT Algorithm
    """
    def __init__(self, _id, _type, layer = 0):
        self.nodeId = _id
        self.nodeType = _type
        self.layer = layer
        self.isConnected = False
        self.connections = []
        self.value = 0

    def reset(self):
        self.value = 0

    def clear(self):
        self.connections = []

    def addConnection(self, connection):
        self.connections.append(connection)

    def getLayer(self):
        return self.layer

    def forward(self):
        for connection in self.connections:
            connection.forward()

    def setValue(self, val):
        self.value = val

    def clone(self):
        new = Node(
            deepcopy(self.nodeId), 
            deepcopy(self.nodeType), 
            deepcopy(self.layer)
        )

        new.isConnected = deepcopy(self.isConnected)

        return new

    def __eq__(self, other):
        return ((self.nodeType, self.nodeId) == (other.nodeType, other.nodeId))

    def __repr__(self):
        return f'Node: ID - {self.nodeId}, Type - {self.nodeType}, Layer - {self.layer}'