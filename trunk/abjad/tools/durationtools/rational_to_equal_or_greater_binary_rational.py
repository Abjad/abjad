from fractions import Fraction
import math


def rational_to_equal_or_greater_binary_rational(rational):
    '''.. versionadded:: 1.1

    Change `rational` to equal to greater binary rational::

        abjad> from abjad.tools import durationtools

    ::

        abjad> for n in range(1, 17): # doctest: +SKIP
        ...     rational = Fraction(n, 16)
        ...     written_duration = durationtools.rational_to_equal_or_greater_binary_rational(rational)
        ...     print '%s/16\\t%s' % (n, written_duration)
        ...
        1/16    1/16
        2/16    1/8
        3/16    1/4
        4/16    1/4
        5/16    1/2
        6/16    1/2
        7/16    1/2
        8/16    1/2
        9/16    1
        10/16   1
        11/16   1
        12/16   1
        13/16   1
        14/16   1
        15/16   1
        16/16   1

    ::

        abjad> durationtools.rational_to_equal_or_greater_binary_rational(Fraction(1, 80))
        Fraction(1, 64)

    ::

        abjad> durationtools.rational_to_equal_or_greater_binary_rational(Fraction(17, 16))
        Fraction(2, 1)

    Use to find written duration of tupletted leaves.

    Return fraction.

    .. versionchanged:: 2.0
        renamed ``durationtools.naive_prolated_to_written_not_less_than()`` to
        ``durationtools.rational_to_equal_or_greater_binary_rational()``.
    '''

    # find exponent of denominator
    exponent = -int(math.ceil(math.log(rational, 2)))

    # find numerator, denominator and written duration
    written_duration = Fraction(1, 2) ** exponent

    # return written duration
    return written_duration
