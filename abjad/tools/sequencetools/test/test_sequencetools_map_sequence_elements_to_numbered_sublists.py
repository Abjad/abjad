# -*- encoding: utf-8 -*-
from abjad import *


def test_sequencetools_map_sequence_elements_to_numbered_sublists_01():

    sequence_2 = sequencetools.map_sequence_elements_to_numbered_sublists([1, 2, -3, -4, 5])

    assert sequence_2 == [[1], [2, 3], [-4, -5, -6], [-7, -8, -9, -10], [11, 12, 13, 14, 15]]


def test_sequencetools_map_sequence_elements_to_numbered_sublists_02():

    sequence_2 = sequencetools.map_sequence_elements_to_numbered_sublists([1, 0, -3, -4, 5])

    assert sequence_2 == [[1], [], [-2, -3, -4], [-5, -6, -7, -8], [9, 10, 11, 12, 13]]
