from abjad import *
from abjad.tools import sequencetools


def test_sequencetools_CyclicTree___iter___01():
    '''Empty cyclic tree iterates no elements.
    '''

    cyclic_tree = sequencetools.CyclicTree([])

    for element in cyclic_tree:
        assert False


def test_sequencetools_CyclicTree___iter___02():
    '''Cyclic tree iterates top-level elements only once.
    '''

    cyclic_tree = sequencetools.CyclicTree([[1, 2], [3, 4]])
    elements = list(iter(cyclic_tree))

    assert elements[0] is cyclic_tree[0]
    assert elements[1] is cyclic_tree[1]
