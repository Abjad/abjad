from abjad import *
from abjad.tools import seqtools


def test_seqtools_retain_sequence_elements_at_indices_cyclically_01():

    t = seqtools.retain_sequence_elements_at_indices_cyclically(range(20), [0, 1], 5)
    assert t == [0, 1, 5, 6, 10, 11, 15, 16]


def test_seqtools_retain_sequence_elements_at_indices_cyclically_02():

    t = seqtools.retain_sequence_elements_at_indices_cyclically(range(20), [0, 1], 5, 1)
    assert t == [1, 2, 6, 7, 11, 12, 16, 17]
