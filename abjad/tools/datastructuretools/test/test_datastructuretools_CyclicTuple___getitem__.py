# -*- coding: utf-8 -*-
from abjad import *


def test_datastructuretools_CyclicTuple___getitem___01():

    cyclic_tuple = datastructuretools.CyclicTuple(range(3))

    assert cyclic_tuple[0] == 0
    assert cyclic_tuple[1] == 1
    assert cyclic_tuple[2] == 2
    assert cyclic_tuple[3] == 0
    assert cyclic_tuple[4] == 1
    assert cyclic_tuple[5] == 2


def test_datastructuretools_CyclicTuple___getitem___02():

    cyclic_tuple = datastructuretools.CyclicTuple(range(3))

    assert cyclic_tuple[-0] == 0
    assert cyclic_tuple[-1] == 2
    assert cyclic_tuple[-2] == 1
    assert cyclic_tuple[-3] == 0
    assert cyclic_tuple[-4] == 2
    assert cyclic_tuple[-5] == 1
