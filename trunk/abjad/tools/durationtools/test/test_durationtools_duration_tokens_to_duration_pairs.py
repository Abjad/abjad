from abjad import *
from abjad.tools import durationtools


def test_durationtools_duration_tokens_to_duration_pairs_01():

    pairs = durationtools.duration_tokens_to_duration_pairs([Fraction(2, 4), 3, '8.', (5, 16)])

    assert pairs == [(1, 2), (3, 1), (3, 16), (5, 16)]
