from abjad.tools import mathtools


def duration_tokens_to_least_common_denominator(duration_tokens):
    '''.. versionadded:: 2.0

    Change `duration_tokens` to least common denominator::

        >>> durationtools.duration_tokens_to_least_common_denominator(
        ...     [Fraction(2, 4), 3, '8.', (5, 16)])
        16

    Return positive integer.
    '''
    from abjad.tools import durationtools

    denominators = [durationtools.Duration(x).denominator for x in duration_tokens]

    return mathtools.least_common_multiple(*denominators)
