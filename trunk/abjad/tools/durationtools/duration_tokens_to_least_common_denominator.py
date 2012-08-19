from abjad.tools import mathtools


def duration_tokens_to_least_common_denominator(duration_tokens):
    '''.. versionadded:: 2.0

    Change `duration_tokens` to least common denominator::

        >>> from abjad.tools import durationtools

    ::

        >>> durationtools.duration_tokens_to_least_common_denominator(
        ...     [Fraction(2, 4), 3, '8.', (5, 16)])
        16

    Return positive integer.
    '''
    from abjad.tools import durationtools

    duration_pairs = durationtools.duration_tokens_to_duration_pairs(duration_tokens)
    denominators = [pair[1] for pair in duration_pairs]

    return mathtools.least_common_multiple(*denominators)
