# ================================
# Author: Kristian N Jensen
# Date: 23/10 - 18
# Project: NEAT
# ================================

# * Custom Libraries 
from NEATWrapper import Connection
from NEATWrapper import Node

# * Third-party libraries
import pytest

@pytest.fixture
def connection():
    _in = Node(1, 'input', layer=1)
    _out = Node(2, 'out', layer=2)
    weight = 2
    return Connection(_in, _out, weight)


def test_standard_init(connection):
    assert connection.weight == 2
    assert connection.innovation == 0
