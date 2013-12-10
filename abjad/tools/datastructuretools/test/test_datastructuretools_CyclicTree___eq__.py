# -*- encoding: utf-8 -*-
from abjad import *


def test_datastructuretools_CyclicTree___eq___01():

    cyclic_tree_1 = datastructuretools.CyclicPayloadTree([[1, 2], [3, 4]])
    cyclic_tree_2 = datastructuretools.CyclicPayloadTree([[1, 2], [3, 4]])
    cyclic_tree_3 = datastructuretools.CyclicPayloadTree([[5, 6], [7, 8]])

    assert     cyclic_tree_1 == cyclic_tree_2
    assert not cyclic_tree_1 == cyclic_tree_3
    assert not cyclic_tree_2 == cyclic_tree_3
