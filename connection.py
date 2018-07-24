# ================================
# Author: Kristian N Jensen
# Date: 24/07 - 18
# Project: NEAT
# ================================


class Connection:
    """
    Class for a Connection in the NEAT Algorithm
    """
    def __init__(self, _in, _out, weight, innovation):
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

    def __repr__(self):
        return "Connection: inNode - {}, outNode - {}, weight - {}, innovation - {}".format(
            self.inNode, self.outNode, self.weight, self.innovation
        )