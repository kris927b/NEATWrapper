# ================================
# Author: Kristian N Jensen
# Date: 24/07 - 18
# Project: NEAT
# ================================

# Built-in Libraries
from random import random, uniform
from math import e
from copy import copy

class Connection:
    """Connection - This is a Connection object, to store informatioon about a connection between two nodes. 
        
        This object, stores the information of the two connected nodes, the weight of the connection and the innovation number. Moreover, the object contains methods for computing the forward pass of this connection and doing mutation of the weights.
        
        Args:
            _in (Node): Node object that the information has to flow from.
            _out (Node): Node object that the information has to flow to.
            weight (Float): Float value of the weight assigned to this connection.
            innovation (int, optional): Defaults to 0. Innovation number of this type of connection.
        """
    def __init__(self, _in, _out, weight, innovation=0):
        self.inNode = _in
        self.outNode = _out
        self.weight = weight
        self.enabled = True
        self.innovation = innovation

    def forward(self):
        if not self.enabled:
            return
        _input = self.inNode.value
        output = _input * self.weight
        output = self.relu(output)
        self.outNode.value += output

    def sigmoid(self, x):
        y = 1 / (1 + e**(-x))
        return y

    def relu(self, x):
        y = max(x, 0)
        return y

    def setInnovationNo(self, number):
        self.innovation = number

    def getInnovationNo(self):
        return self.innovation

    def mutateWeights(self):
        r = random()
        if r <= 0.5:
            self.weight += uniform(-0.5, 0.5)
        else:
            self.weight = uniform(-2, 2)

    def clone(self, enabled):
        new = Connection(
            self.inNode.clone(), 
            self.outNode.clone(), 
            copy(self.weight), 
            innovation=copy(self.innovation)
        )

        new.enabled = enabled

        return new

    def __eq__(self, conn2):
        return ((self.inNode, self.outNode) == (conn2.inNode, conn2.outNode))

    def __repr__(self):
        return "Connection: \n ==> inNode - {}, \n ==> outNode - {}, \n ==> weight - {}, \n ==> innovation - {}".format(
            self.inNode, self.outNode, self.weight, self.innovation
        )