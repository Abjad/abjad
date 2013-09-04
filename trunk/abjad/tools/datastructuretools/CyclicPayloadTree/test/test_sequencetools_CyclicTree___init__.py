# -*- encoding: utf-8 -*-
from abjad import *


def test_sequencetools_CyclicTree___init___01():
    r'''Initialize cyclic tree from other cyclic tree.
    '''

    tree_1 = datastructuretools.CyclicPayloadTree([[4, 5], [6, 7]])
    tree_2 = datastructuretools.CyclicPayloadTree(tree_1)

    assert tree_1 is not tree_2
    assert tree_1 == tree_2
