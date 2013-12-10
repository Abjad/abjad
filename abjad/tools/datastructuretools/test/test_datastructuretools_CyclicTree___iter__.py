# -*- encoding: utf-8 -*-
from abjad import *


def test_datastructuretools_CyclicTree___iter___01():
    r'''Empty cyclic tree iterates no elements.
    '''

    cyclic_tree = datastructuretools.CyclicPayloadTree([])

    for element in cyclic_tree:
        assert False


def test_datastructuretools_CyclicTree___iter___02():
    r'''Cyclic tree iterates top-level elements only once.
    '''

    cyclic_tree = datastructuretools.CyclicPayloadTree([[1, 2], [3, 4]])
    elements = list(iter(cyclic_tree))

    assert elements[0] is cyclic_tree[0]
    assert elements[1] is cyclic_tree[1]
