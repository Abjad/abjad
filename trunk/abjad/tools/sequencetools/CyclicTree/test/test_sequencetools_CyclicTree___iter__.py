from abjad import *
from abjad.tools import sequencetools


def test_sequencetools_CyclicTree___iter___01():
    '''Empty cyclic tree iterates no elements.
    '''

    cyclic_tree = sequencetools.CyclicTree([])

    for element in cyclic_tree:
        assert False
