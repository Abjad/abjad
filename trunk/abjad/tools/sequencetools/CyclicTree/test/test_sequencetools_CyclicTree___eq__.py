from abjad import *
from abjad.tools import sequencetools


def test_sequencetools_CyclicTree___eq___01():

    cyclic_tree_1 = sequencetools.CyclicTree([[1, 2], [3, 4]])
    cyclic_tree_2 = sequencetools.CyclicTree([[1, 2], [3, 4]])
    cyclic_tree_3 = sequencetools.CyclicTree([[5, 6], [7, 8]])

    assert     cyclic_tree_1 == cyclic_tree_2
    assert not cyclic_tree_1 == cyclic_tree_3
    assert not cyclic_tree_2 == cyclic_tree_3
