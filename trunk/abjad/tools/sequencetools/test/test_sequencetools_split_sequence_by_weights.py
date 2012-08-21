from abjad import *


def test_sequencetools_split_sequence_by_weights_01():

    sequence = (10, -10, 10, -10)
    pieces = sequencetools.split_sequence_by_weights(
        sequence, [3, 15, 3], cyclic=True, overhang=True)

    assert pieces == [(3,), (7, -8), (-2, 1), (3,), (6, -9), (-1,)]


def test_sequencetools_split_sequence_by_weights_02():
    '''Even split with overhang produces no terminal empty piece.
    '''

    sequence = (10, -10, 10, -10)
    pieces = sequencetools.split_sequence_by_weights(
        sequence, [20], cyclic=True, overhang=True)

    assert pieces == [(10, -10), (10, -10)]


def test_sequencetools_split_sequence_by_weights_03():

    sequence = (10, -10, 10, -10)
    pieces = sequencetools.split_sequence_by_weights(
        sequence, [3, 15, 3], cyclic=True, overhang=False)

    assert pieces == [(3,), (7, -8), (-2, 1), (3,), (6, -9)] 


def test_sequencetools_split_sequence_by_weights_04():

    sequence = (10, -10, 10, -10)
    pieces = sequencetools.split_sequence_by_weights(
        sequence, [3, 15, 3], cyclic=False, overhang=True)

    assert pieces == [(3,), (7, -8), (-2, 1), (9, -10)]


def test_sequencetools_split_sequence_by_weights_05():
    '''Even split with overhang produces no terminal empty piece.
    '''

    sequence = (10, -10, 10, -10)
    pieces = sequencetools.split_sequence_by_weights(
        sequence, [20], cyclic=False, overhang=True)

    assert pieces == [(10, -10), (10, -10)]


def test_sequencetools_split_sequence_by_weights_06():

    sequence = (10, -10, 10, -10)
    pieces = sequencetools.split_sequence_by_weights(
        sequence, [3, 15, 3], cyclic=False, overhang=False)

    assert pieces == [(3, ), (7, -8), (-2, 1)]
