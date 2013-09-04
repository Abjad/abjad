# -*- encoding: utf-8 -*-
from abjad import *


def test_PayloadTree___init___01():
    r'''Initialize tree from other tree.
    '''

    tree_1 = sequencetools.PayloadTree([[4, 5], [6, 7]])
    tree_2 = sequencetools.PayloadTree(tree_1)

    assert tree_1 is not tree_2
    assert tree_1 == tree_2
