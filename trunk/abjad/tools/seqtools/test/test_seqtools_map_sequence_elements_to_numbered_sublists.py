from abjad import *
from abjad.tools import seqtools


def test_seqtools_map_sequence_elements_to_numbered_sublists_01():

    t = seqtools.map_sequence_elements_to_numbered_sublists([1, 2, -3, -4, 5])

    assert t == [[1], [2, 3], [-4, -5, -6], [-7, -8, -9, -10], [11, 12, 13, 14, 15]]


def test_seqtools_map_sequence_elements_to_numbered_sublists_02():

    t = seqtools.map_sequence_elements_to_numbered_sublists([1, 0, -3, -4, 5])

    assert t == [[1], [ ], [-2, -3, -4], [-5, -6, -7, -8], [9, 10, 11, 12, 13]]
