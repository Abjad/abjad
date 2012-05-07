from abjad import *
from abjad.tools.mathtools import NonreducedFraction
from abjad.tools import sequencetools


def test_sequencetools_repeat_sequence_to_weight_exactly_01():

    assert sequencetools.repeat_sequence_to_weight_exactly((5, -5, -5), 23) == (5, -5, -5, 5, -3)


def test_sequencetools_repeat_sequence_to_weight_exactly_02():
    '''Works with nonreduced fractions.
    '''

    sequence = sequencetools.repeat_sequence_to_weight_exactly([NonreducedFraction(3, 16)], 1)

    assert sum(sequence) == 1
    assert sequence == [
        NonreducedFraction(3, 16), NonreducedFraction(3, 16), NonreducedFraction(3, 16), 
        NonreducedFraction(3, 16), NonreducedFraction(3, 16), NonreducedFraction(1, 16)]
