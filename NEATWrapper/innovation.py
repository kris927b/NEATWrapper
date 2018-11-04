# ================================
# Author: Kristian N Jensen
# Date: 24/07 - 18
# Project: NEAT
# ================================

# Built-in Libraries
from copy import deepcopy
import random

# Custom Libraries
from NEATWrapper.connection import Connection

class Innovation:
    """
    Class to store innovations in the NEAT Algorithm
    """
    def __init__(self):
        self.connectionsDone = []
        self.innoNo = 1

    def checkConnection(self, node1, node2, weight=None):
        newConnection = Connection(node1,
            node2,
            weight=weight if weight else random.uniform(-2, 2)
        )
        gotInnovation = False
        for connection in self.connectionsDone:
            if connection == newConnection:
                inno = connection.getInnovationNo()
                newConnection.setInnovationNo(deepcopy(inno))
                gotInnovation = True
                break

        if not gotInnovation:
            newConnection.setInnovationNo(deepcopy(self.innoNo))
            self.connectionsDone.append(newConnection)
            self.innoNo += 1

        return newConnection

    def __repr__(self):
        return "Innovation History: {}".format(self.connectionsDone)

    