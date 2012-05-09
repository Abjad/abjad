from abjad import *
from abjad.tools.mathtools import NonreducedFraction
from abjad.tools import sequencetools


def test_sequencetools_repeat_sequence_to_weight_exactly_01():

    assert sequencetools.repeat_sequence_to_weight_exactly((5, -5, -5), 23) == (5, -5, -5, 5, -3)


def test_sequencetools_repeat_sequence_to_weight_exactly_02():
    '''Works with nonreduced fractions.
    '''

    sequence = [NonreducedFraction(3, 16)]
    sequence = sequencetools.repeat_sequence_to_weight_exactly(sequence, NonreducedFraction(5, 4))

    assert sum(sequence) == NonreducedFraction(5, 4)
    assert [x.pair for x in sequence] == [(3, 16), (3, 16), (3, 16), (3, 16), (3, 16), (3, 16), (2, 16)]
