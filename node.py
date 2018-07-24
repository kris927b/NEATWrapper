# ================================
# Author: Kristian N Jensen
# Date: 24/07 - 18
# Project: NEAT
# ================================


class Node:
    """
    Class for a Node in the NEAT Algorithm
    """
    def __init__(self, _id, _type):
        self.nodeId = _id
        self.nodeType = _type
        self.isConnected = False
        self.connections = []
        self.value = 0

    def clear(self):
        self.value = 0

    def __repr__(self):
        return "Node: ID - {}, Type - {}".format(self.nodeId, self.nodeType)