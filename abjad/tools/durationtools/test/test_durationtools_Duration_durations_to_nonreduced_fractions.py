# -*- coding: utf-8 -*-
from abjad import *


def test_durationtools_Duration_durations_to_nonreduced_fractions_01():

    durations = [Fraction(2, 4), 3, (5, 16)]

    result = Duration.durations_to_nonreduced_fractions(durations)

    pairs = [
        mathtools.NonreducedFraction(x)
        for x in [(8, 16), (48, 16), (5, 16)]
        ]

    assert result == pairs
