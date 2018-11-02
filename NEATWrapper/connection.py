# ================================
# Author: Kristian N Jensen
# Date: 24/07 - 18
# Project: NEAT
# ================================

# Built-in Libraries
from random import random, uniform
from math import e
from copy import deepcopy

class Connection:
    """
    Class for a Connection in the NEAT Algorithm
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
            deepcopy(self.inNode), 
            deepcopy(self.outNode), 
            deepcopy(self.weight), 
            innovation=deepcopy(self.innovation)
        )

        new.enabled = enabled

        return new

    def __eq__(self, conn2):
        return ((self.inNode, self.outNode) == (conn2.inNode, conn2.outNode))

    def __repr__(self):
        return "Connection: \n ==> inNode - {}, \n ==> outNode - {}, \n ==> weight - {}, \n ==> innovation - {}".format(
            self.inNode, self.outNode, self.weight, self.innovation
        )