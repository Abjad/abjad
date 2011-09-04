from abjad import *
from abjad.tools import sequencetools


def test_sequencetools_map_sequence_elements_to_numbered_sublists_01():

    t = sequencetools.map_sequence_elements_to_numbered_sublists([1, 2, -3, -4, 5])

    assert t == [[1], [2, 3], [-4, -5, -6], [-7, -8, -9, -10], [11, 12, 13, 14, 15]]


def test_sequencetools_map_sequence_elements_to_numbered_sublists_02():

    t = sequencetools.map_sequence_elements_to_numbered_sublists([1, 0, -3, -4, 5])

    assert t == [[1], [], [-2, -3, -4], [-5, -6, -7, -8], [9, 10, 11, 12, 13]]
