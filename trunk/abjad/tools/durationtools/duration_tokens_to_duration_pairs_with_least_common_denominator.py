from abjad.tools import mathtools


def duration_tokens_to_duration_pairs_with_least_common_denominator(durations):
    '''.. versionadded:: 2.0

    Change `durations` to nonreduced fractions with least common denominator::

        >>> durationtools.duration_tokens_to_duration_pairs_with_least_common_denominator(
        ... [Fraction(2, 4), 3, '8.', (5, 16)])
        [NonreducedFraction(8, 16), NonreducedFraction(48, 16), NonreducedFraction(3, 16), NonreducedFraction(5, 16)]

    Return new object of `duration_tokens` type.
    '''
    from abjad.tools import durationtools

    durations = [durationtools.Duration(x) for x in durations]
    denominators = [duration.denominator for duration in durations]
    lcd = mathtools.least_common_multiple(*denominators)

    nonreduced_fractions = [mathtools.NonreducedFraction(x).with_denominator(lcd) for x in durations]
    result = type(durations)(nonreduced_fractions)

    return result
