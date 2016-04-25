# -*- coding: utf-8 -*-
from abjad import *


def test_sequencetools_repeat_sequence_to_weight_01():

    assert sequencetools.repeat_sequence_to_weight((5, -5, -5), 23) == (5, -5, -5, 5, -3)


def test_sequencetools_repeat_sequence_to_weight_02():
    r'''Works with nonreduced fractions.
    '''

    sequence = [mathtools.NonreducedFraction(3, 16)]
    sequence = sequencetools.repeat_sequence_to_weight(
        sequence,
        mathtools.NonreducedFraction(5, 4),
        )

    assert sum(sequence) == mathtools.NonreducedFraction(5, 4)
    assert [x.pair for x in sequence] == [(3, 16), (3, 16), (3, 16), (3, 16), (3, 16), (3, 16), (2, 16)]
