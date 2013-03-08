from abjad import *


def test_CyclicTree___init___01():
    '''Initialize cyclic tree from other cyclic tree.
    '''

    tree_1 = sequencetools.CyclicTree([[4, 5], [6, 7]])
    tree_2 = sequencetools.CyclicTree(tree_1)

    assert tree_1 is not tree_2
    assert tree_1 == tree_2
