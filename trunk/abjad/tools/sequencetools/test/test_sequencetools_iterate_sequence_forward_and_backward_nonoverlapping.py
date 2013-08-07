# -*- encoding: utf-8 -*-
from abjad import *


def test_sequencetools_iterate_sequence_forward_and_backward_nonoverlapping_01():

    sequence_2 = list(sequencetools.iterate_sequence_forward_and_backward_nonoverlapping(xrange(1, 6)))

    assert sequence_2 == [1, 2, 3, 4, 5, 5, 4, 3, 2, 1]
