# ================================
# Author: Kristian N Jensen
# Date: 24/07 - 18
# Project: NEAT
# ================================

# Built-in Libraries
from copy import deepcopy
import random

# Custom Libraries
from connection import Connection

class Innovation:
    """
    Class to store innovations in the NEAT Algorithm
    """
    def __init__(self):
        self.connectionsDone = []
        self.innoNo = 0

    def checkConnection(self, node1, node2):
        newConnection = Connection(node1,
            node2,
            weight=random.randint(-2, 2)
        )
        gotInnovation = False
        for connection in self.connectionsDone:
            if connection == newConnection:
                inno = connection.getInnovationNo()
                newConnection.setInnovationNo(deepcopy(inno))
                gotInnovation = True
                break

        if not gotInnovation:
            self.innoNo += 1
            newConnection.setInnovationNo(deepcopy(self.innoNo))
            self.connectionsDone.append(newConnection)

        return newConnection

    def __repr__(self):
        return "Innovation History: {}".format(self.connectionsDone)

    