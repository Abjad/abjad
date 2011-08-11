from abjad import *
from abjad.tools import seqtools


def test_seqtools_get_sequence_elements_frequency_distribution_01( ):

    sequence = [2, 2, 2, 1, 2, 3, 3, 3, 1, 1, 2, 3, 3, 3, 1, 2, 2, 3, 1, 1, 1, 1]
    frequency_distribution = seqtools.get_sequence_elements_frequency_distribution(sequence)
    assert frequency_distribution == [(1, 8), (2, 7), (3, 7)]
