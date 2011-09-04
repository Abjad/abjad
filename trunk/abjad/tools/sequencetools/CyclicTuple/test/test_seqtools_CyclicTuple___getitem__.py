from abjad import *
from abjad.tools import sequencetools


def test_seqtools_CyclicTuple___getitem___01():

    cyclic_tuple = sequencetools.CyclicTuple(range(3))

    assert cyclic_tuple[0] == 0
    assert cyclic_tuple[1] == 1
    assert cyclic_tuple[2] == 2
    assert cyclic_tuple[3] == 0
    assert cyclic_tuple[4] == 1
    assert cyclic_tuple[5] == 2


def test_seqtools_CyclicTuple___getitem___02():

    cyclic_tuple = sequencetools.CyclicTuple(range(3))

    assert cyclic_tuple[-0] == 0
    assert cyclic_tuple[-1] == 2
    assert cyclic_tuple[-2] == 1
    assert cyclic_tuple[-3] == 0
    assert cyclic_tuple[-4] == 2
    assert cyclic_tuple[-5] == 1
