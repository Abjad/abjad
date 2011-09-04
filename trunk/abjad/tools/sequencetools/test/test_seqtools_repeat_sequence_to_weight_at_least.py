from abjad import *
from abjad.tools import sequencetools


def test_sequencetools_repeat_sequence_to_weight_at_least_01():

    assert sequencetools.repeat_sequence_to_weight_at_least((5, -5, -5), 23) == (5, -5, -5, 5, -5)
