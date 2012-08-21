from abjad import *


def test_sequencetools_split_sequence_extended_to_weights_01():

    parts = sequencetools.split_sequence_extended_to_weights([1, 2, 3, 4, 5], [7, 7, 7], overhang=True)
    assert parts == [[1, 2, 3, 1], [3, 4], [1, 1, 2, 3], [4, 5]]


def test_sequencetools_split_sequence_extended_to_weights_02():

    parts = sequencetools.split_sequence_extended_to_weights([1, 2, 3, 4, 5], [7, 7, 7], overhang=False)
    assert parts == [[1, 2, 3, 1], [3, 4], [1, 1, 2, 3]]
