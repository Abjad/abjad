from abjad.tools import *


def test_sequencetools_partition_sequence_by_backgrounded_weights_01():

    assert sequencetools.partition_sequence_by_backgrounded_weights(
        [-5, -15, -10], [20, 10]) == [[-5, -15], [-10]]

    assert sequencetools.partition_sequence_by_backgrounded_weights(
        [-5, -15, -10], [5, 5, 5, 5, 5, 5]) == [[-5], [-15], [], [], [-10], []]

    assert sequencetools.partition_sequence_by_backgrounded_weights(
        [-5, -15, -10], [1, 29]) == [[-5], [-15, -10]]

    assert sequencetools.partition_sequence_by_backgrounded_weights(
        [-5, -15, -10], [2, 28]) == [[-5], [-15, -10]]

    assert sequencetools.partition_sequence_by_backgrounded_weights(
        [-5, -15, -10], [1, 1, 1, 1, 1, 25]) == [[-5], [], [], [], [], [-15, -10]]
