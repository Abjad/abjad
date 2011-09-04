from abjad.tools import sequencetools
from abjad import *


def test_sequencetools_overwrite_sequence_elements_at_indices_01():

    l = range(10)
    t = sequencetools.overwrite_sequence_elements_at_indices(l, [(0, 3), (5, 3)])

    assert t == [0, 0, 0, 3, 4, 5, 5, 5, 8, 9]


def test_sequencetools_overwrite_sequence_elements_at_indices_02():

    l = range(10)
    t = sequencetools.overwrite_sequence_elements_at_indices(l, [(0, 99)])

    assert t == [0, 0, 0, 0, 0, 0, 0, 0, 0, 0]
