# ================================
# Author: Kristian N Jensen
# Date: 24/07 - 18
# Project: NEAT
# ================================


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
        _input = self.inNode.value
        output = _input * self.weight
        output = max(output, 0)
        self.outNode.value += output

    def setInnovationNo(self, number):
        self.innovation = number

    def getInnovationNo(self):
        return self.innovation

    def __eq__(self, conn2):
        return ((self.inNode, self.outNode) == (conn2.inNode, conn2.outNode))

    def __repr__(self):
        return "Connection: \n ==> inNode - {}, \n ==> outNode - {}, \n ==> weight - {}, \n ==> innovation - {}".format(
            self.inNode, self.outNode, self.weight, self.innovation
        )