from abjad import *
from abjad.tools import durtools


def test_durtools_duration_tokens_to_duration_pairs_with_least_common_denominator_01( ):

    tokens = [Fraction(2, 4), 3, '8.', (5, 16)]
    pairs = durtools.duration_tokens_to_duration_pairs_with_least_common_denominator(tokens)

    assert pairs == [(8, 16), (48, 16), (3, 16), (5, 16)]

