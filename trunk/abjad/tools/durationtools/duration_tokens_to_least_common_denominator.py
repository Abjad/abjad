from abjad.tools import mathtools
from abjad.tools.durationtools.duration_tokens_to_duration_pairs import duration_tokens_to_duration_pairs


def duration_tokens_to_least_common_denominator(duration_tokens):
    '''.. versionadded:: 2.0

    Change `duration_tokens` to least common denominator::

        abjad> from abjad.tools import durationtools

    ::

        abjad> durationtools.duration_tokens_to_least_common_denominator([Fraction(2, 4), 3, '8.', (5, 16)])
        16

    Return positive integer.
    '''

    duration_pairs = duration_tokens_to_duration_pairs(duration_tokens)
    denominators = [pair[1] for pair in duration_pairs]

    return mathtools.least_common_multiple(*denominators)
