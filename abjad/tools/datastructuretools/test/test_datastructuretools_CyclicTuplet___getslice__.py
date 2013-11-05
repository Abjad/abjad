# -*- encoding: utf-8 -*-
from abjad import *
from abjad.tools import sequencetools
import py.test


def test_datastructuretools_CyclicTuplet___getslice___01():

    cyclic_tuple = datastructuretools.CyclicTuple(range(3))

    assert cyclic_tuple[:2] == (0, 1)
    assert cyclic_tuple[:10] == (0, 1, 2, 0, 1, 2, 0, 1, 2, 0)
    assert cyclic_tuple[2:10] == (2, 0, 1, 2, 0, 1, 2, 0)
