from abjad.tools import seqtools
from abjad import *


def test_seqtools_overwrite_sequence_elements_at_indices_01():

    l = range(10)
    t = seqtools.overwrite_sequence_elements_at_indices(l, [(0, 3), (5, 3)])

    assert t == [0, 0, 0, 3, 4, 5, 5, 5, 8, 9]


def test_seqtools_overwrite_sequence_elements_at_indices_02():

    l = range(10)
    t = seqtools.overwrite_sequence_elements_at_indices(l, [(0, 99)])

    assert t == [0, 0, 0, 0, 0, 0, 0, 0, 0, 0]
