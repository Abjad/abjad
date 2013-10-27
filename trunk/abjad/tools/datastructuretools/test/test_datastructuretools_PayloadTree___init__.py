# -*- encoding: utf-8 -*-
from abjad import *


def test_datastructuretools_PayloadTree___init___01():
    r'''Initialize tree from other tree.
    '''

    tree_1 = datastructuretools.PayloadTree([[4, 5], [6, 7]])
    tree_2 = datastructuretools.PayloadTree(tree_1)

    assert tree_1 is not tree_2
    assert tree_1 == tree_2
