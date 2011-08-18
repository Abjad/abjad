from abjad import *
from abjad.tools import seqtools


def test_seqtools_get_sequence_elements_at_indices_01():

    sequence = 'string of text'
    assert seqtools.get_sequence_elements_at_indices(sequence, (2, 3, 10, 12)) == (
        'r', 'i', 't', 'x')
