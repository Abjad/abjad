from abjad import *
from abjad.tools import durationtools


def test_durationtools_duration_tokens_to_least_common_denominator_01():

    tokens = [Fraction(2, 4), 3, '8.', (5, 16)]

    assert durationtools.duration_tokens_to_least_common_denominator(tokens) == 16
