from abjad import *
from abjad.tools import sequencetools


def test_sequencetools_reverse_sequence_elements_01():
    '''Reverse sequence elements.
    '''

    result = sequencetools.reverse_sequence_elements([1, (2, 3, 4), 5, (6, 7)])
    assert result == [1, (4, 3, 2), 5, (7, 6)]
