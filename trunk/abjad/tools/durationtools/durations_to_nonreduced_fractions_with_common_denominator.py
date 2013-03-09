from abjad.tools import mathtools


def durations_to_nonreduced_fractions_with_common_denominator(durations):
    '''.. versionadded:: 2.0

    Change `durations` to nonreduced fractions with least common denominator::

        >>> durations = [Duration(2, 4), 3, (5, 16)]
        >>> for x in durationtools.durations_to_nonreduced_fractions_with_common_denominator(
        ...     durations):
        ...     x
        ...
        NonreducedFraction(8, 16)
        NonreducedFraction(48, 16)
        NonreducedFraction(5, 16)

    Return new object of `durations` type.
    '''
    from abjad.tools import durationtools

    durations = [durationtools.Duration(x) for x in durations]
    denominators = [duration.denominator for duration in durations]
    lcd = mathtools.least_common_multiple(*denominators)

    nonreduced_fractions = [mathtools.NonreducedFraction(x).with_denominator(lcd) for x in durations]
    result = type(durations)(nonreduced_fractions)

    return result
