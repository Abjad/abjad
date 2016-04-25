# -*- coding: utf-8 -*-
from abjad import *


def test_datastructuretools_CyclicTuple___getslice___01():

    cyclic_tuple = datastructuretools.CyclicTuple(range(3))

    assert cyclic_tuple[:2] == (0, 1)
    assert cyclic_tuple[:10] == (0, 1, 2, 0, 1, 2, 0, 1, 2, 0)
    assert cyclic_tuple[2:10] == (2, 0, 1, 2, 0, 1, 2, 0)
    assert cyclic_tuple[1:-1] == (1,)
