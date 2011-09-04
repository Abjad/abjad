from abjad import *
from abjad.tools import sequencetools


def test_sequencetools_get_sequence_elements_at_indices_01():

    sequence = 'string of text'
    assert sequencetools.get_sequence_elements_at_indices(sequence, (2, 3, 10, 12)) == (
        'r', 'i', 't', 'x')
