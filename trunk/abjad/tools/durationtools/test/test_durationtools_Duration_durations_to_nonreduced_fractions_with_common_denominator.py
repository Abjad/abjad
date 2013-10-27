# -*- encoding: utf-8 -*-
from abjad import *


def test_durationtools_Duration_durations_to_nonreduced_fractions_with_common_denominator_01():

    durations = [Fraction(2, 4), 3, (5, 16)]
    Duration = durationtools.Duration

    result = \
        Duration.durations_to_nonreduced_fractions_with_common_denominator(
        durations)

    pairs = [
        mathtools.NonreducedFraction(x) 
        for x in [(8, 16), (48, 16), (5, 16)]
        ]

    assert result == pairs
