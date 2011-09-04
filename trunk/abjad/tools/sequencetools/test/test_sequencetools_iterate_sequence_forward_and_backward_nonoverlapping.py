from abjad import *
from abjad.tools import sequencetools


def test_sequencetools_iterate_sequence_forward_and_backward_nonoverlapping_01():

    t = list(sequencetools.iterate_sequence_forward_and_backward_nonoverlapping(xrange(1, 6)))

    assert t == [1, 2, 3, 4, 5, 5, 4, 3, 2, 1]
