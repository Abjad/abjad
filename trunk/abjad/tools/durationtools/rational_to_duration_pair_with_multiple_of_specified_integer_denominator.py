from abjad.tools import mathtools


def rational_to_duration_pair_with_multiple_of_specified_integer_denominator(duration, integer_denominator):
    '''.. versionadded: 1.1.1

    Change `duration` to duration pair with multiple of specified `integer_denominator`::

        >>> durationtools.rational_to_duration_pair_with_multiple_of_specified_integer_denominator(
        ...     Fraction(1, 2), 2)
        NonreducedFraction(1, 2)

    ::

        >>> durationtools.rational_to_duration_pair_with_multiple_of_specified_integer_denominator(
        ...     Fraction(1, 2), 4)
        NonreducedFraction(2, 4)

    ::

        >>> durationtools.rational_to_duration_pair_with_multiple_of_specified_integer_denominator(
        ...     Fraction(1, 2), 8)
        NonreducedFraction(4, 8)

    ::

        >>> durationtools.rational_to_duration_pair_with_multiple_of_specified_integer_denominator(
        ...     Fraction(1, 2), 16)
        NonreducedFraction(8, 16)

    ::

        >>> durationtools.rational_to_duration_pair_with_multiple_of_specified_integer_denominator(
        ...     Fraction(1, 2), 3)
        NonreducedFraction(3, 6)

    ::

        >>> durationtools.rational_to_duration_pair_with_multiple_of_specified_integer_denominator(
        ...     Fraction(1, 2), 6)
        NonreducedFraction(3, 6)

    ::

        >>> durationtools.rational_to_duration_pair_with_multiple_of_specified_integer_denominator(
        ...     Fraction(1, 2), 12)
        NonreducedFraction(6, 12)

    ::

        >>> durationtools.rational_to_duration_pair_with_multiple_of_specified_integer_denominator(
        ...     Fraction(1, 2), 24)
        NonreducedFraction(12, 24)

    ::

        >>> durationtools.rational_to_duration_pair_with_multiple_of_specified_integer_denominator(
        ...     Fraction(1, 2), 5)
        NonreducedFraction(5, 10)

    ::

        >>> durationtools.rational_to_duration_pair_with_multiple_of_specified_integer_denominator(
        ...     Fraction(1, 2), 10)
        NonreducedFraction(5, 10)

    ::

        >>> durationtools.rational_to_duration_pair_with_multiple_of_specified_integer_denominator(
        ...     Fraction(1, 2), 20)
        NonreducedFraction(10, 20)

    ::

        >>> durationtools.rational_to_duration_pair_with_multiple_of_specified_integer_denominator(
        ...     Fraction(1, 2), 40)
        NonreducedFraction(20, 40)

    Return nonreduced fraction.
    '''
    from abjad.tools import durationtools

    pair = mathtools.NonreducedFraction(duration).with_denominator(integer_denominator)

    while not pair.denominator == integer_denominator:
        integer_denominator *= 2
        pair = mathtools.NonreducedFraction(duration).with_denominator(integer_denominator)

    return pair
