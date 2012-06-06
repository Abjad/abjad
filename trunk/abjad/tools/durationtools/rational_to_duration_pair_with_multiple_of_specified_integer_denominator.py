from abjad.tools.durationtools.rational_to_duration_pair_with_specified_integer_denominator import rational_to_duration_pair_with_specified_integer_denominator


def rational_to_duration_pair_with_multiple_of_specified_integer_denominator(
    duration, integer_denominator):
    '''.. versionadded: 1.1.1

    Change `duration` to duration pair with multiple of specified `integer_denominator`::

        >>> from abjad.tools import durationtools

    ::

        >>> durationtools.rational_to_duration_pair_with_multiple_of_specified_integer_denominator(Fraction(1, 2), 2)
        (1, 2)
        >>> durationtools.rational_to_duration_pair_with_multiple_of_specified_integer_denominator(Fraction(1, 2), 4)
        (2, 4)
        >>> durationtools.rational_to_duration_pair_with_multiple_of_specified_integer_denominator(Fraction(1, 2), 8)
        (4, 8)
        >>> durationtools.rational_to_duration_pair_with_multiple_of_specified_integer_denominator(Fraction(1, 2), 16)
        (8, 16)

    ::

        >>> durationtools.rational_to_duration_pair_with_multiple_of_specified_integer_denominator(Fraction(1, 2), 3)
        (3, 6)
        >>> durationtools.rational_to_duration_pair_with_multiple_of_specified_integer_denominator(Fraction(1, 2), 6)
        (3, 6)
        >>> durationtools.rational_to_duration_pair_with_multiple_of_specified_integer_denominator(Fraction(1, 2), 12)
        (6, 12)
        >>> durationtools.rational_to_duration_pair_with_multiple_of_specified_integer_denominator(Fraction(1, 2), 24)
        (12, 24)

    ::

        >>> durationtools.rational_to_duration_pair_with_multiple_of_specified_integer_denominator(Fraction(1, 2), 5)
        (5, 10)
        >>> durationtools.rational_to_duration_pair_with_multiple_of_specified_integer_denominator(Fraction(1, 2), 10)
        (5, 10)
        >>> durationtools.rational_to_duration_pair_with_multiple_of_specified_integer_denominator(Fraction(1, 2), 20)
        (10, 20)
        >>> durationtools.rational_to_duration_pair_with_multiple_of_specified_integer_denominator(Fraction(1, 2), 40)
        (20, 40)

    Return integer pair.

    .. versionchanged:: 2.0
        renamed ``durationtools.in_terms_of_binary_multiple()`` to
        ``durationtools.rational_to_duration_pair_with_multiple_of_specified_integer_denominator()``.
    '''

    pair = rational_to_duration_pair_with_specified_integer_denominator(
        duration, integer_denominator)

    while not pair[-1] == integer_denominator:
        integer_denominator *= 2
        pair = rational_to_duration_pair_with_specified_integer_denominator(
            pair, integer_denominator)

    return pair
