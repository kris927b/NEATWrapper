# ================================
# Author: Kristian N Jensen
# Date: 23/10 - 18
# Project: NEAT
# ================================

# * Third-party libraries
import pytest
import sys

sys.path.append('../')

# * Custom Libraries 
import NEATWrapper

@pytest.fixture
def connection():
    _in = NEATWrapper.Node(1, 'input', layer=1)
    _out = NEATWrapper.Node(2, 'out', layer=2)
    weight = 2
    return NEATWrapper.Connection(_in, _out, weight)


def test_standard_init(connection):
    assert connection.weight == 2
    assert connection.innovation == 0
