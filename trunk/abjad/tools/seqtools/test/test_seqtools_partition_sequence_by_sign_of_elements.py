from abjad import *
from abjad.tools import seqtools


def test_seqtools_partition_sequence_by_sign_of_elements_01( ):

    sequence = (0, 0, -1, -1, 2, 3, -5, 1, 2, 5, -5, -6)

    groups = seqtools.partition_sequence_by_sign_of_elements(sequence)
    assert groups == [(0, 0), (-1, -1), (2, 3), (-5,), (1, 2, 5), (-5, -6)]

    groups = seqtools.partition_sequence_by_sign_of_elements(sequence, sign = [-1])
    assert groups == [0, 0, (-1, -1), 2, 3, (-5,), 1, 2, 5, (-5, -6)]

    groups = seqtools.partition_sequence_by_sign_of_elements(sequence, sign = [0])
    assert groups == [(0, 0), -1, -1, 2, 3, -5, 1, 2, 5, -5, -6]

    groups = seqtools.partition_sequence_by_sign_of_elements(sequence, sign = [1])
    assert groups == [0, 0, -1, -1, (2, 3), -5, (1, 2, 5), -5, -6]

    groups = seqtools.partition_sequence_by_sign_of_elements(sequence, sign = [-1, 0])
    assert groups == [(0, 0), (-1, -1), 2, 3, (-5,), 1, 2, 5, (-5, -6)]

    groups = seqtools.partition_sequence_by_sign_of_elements(sequence, sign = [-1, 1])
    assert groups == [0, 0, (-1, -1), (2, 3), (-5,), (1, 2, 5), (-5, -6)]

    groups = seqtools.partition_sequence_by_sign_of_elements(sequence, sign = [0, 1])
    assert groups == [(0, 0), -1, -1, (2, 3), -5, (1, 2, 5), -5, -6]

    groups = seqtools.partition_sequence_by_sign_of_elements(sequence, sign = [-1, 0, 1])
    assert groups == [(0, 0), (-1, -1), (2, 3), (-5,), (1, 2, 5), (-5, -6)]
