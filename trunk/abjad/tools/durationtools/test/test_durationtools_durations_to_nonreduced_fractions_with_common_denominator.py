from abjad import *


def test_durationtools_durations_to_nonreduced_fractions_with_common_denominator_01():

    tokens = [Fraction(2, 4), 3, (5, 16)]
    pairs = durationtools.durations_to_nonreduced_fractions_with_common_denominator(tokens)

    assert pairs == [mathtools.NonreducedFraction(x) for x in [(8, 16), (48, 16), (5, 16)]]
