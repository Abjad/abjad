from fractions import Fraction
import math


def rational_to_equal_or_lesser_binary_rational(rational):
    '''.. versionadded:: 1.1

    Change `rational` to equal or lesser binary rational::

        abjad> from abjad.tools import durationtools

    ::

        abjad> for n in range(1, 17): # doctest: +SKIP
        ...     rational = Fraction(n, 16)
        ...     written_duration = durationtools.rational_to_equal_or_lesser_binary_rational(rational)
        ...     print '%s/16\\t%s' % (n, written_duration)
        ...
        1/16    1/16
        2/16    1/8
        3/16    1/8
        4/16    1/4
        5/16    1/4
        6/16    1/4
        7/16    1/4
        8/16    1/2
        9/16    1/2
        10/16   1/2
        11/16   1/2
        12/16   1/2
        13/16   1/2
        14/16   1/2
        15/16   1/2
        16/16   1

    ::

        abjad> durationtools.rational_to_equal_or_lesser_binary_rational(Fraction(1, 80))
        Fraction(1, 128)

    Return fraction.

    Function intended to find written duration of notes inside tuplet.

    .. versionchanged:: 2.0
        renamed ``durationtools.naive_prolated_to_written_not_greater_than()`` to
        ``durationtools.rational_to_equal_or_lesser_binary_rational()``.
    '''

    # find exponent of denominator
    exponent = -int(math.floor(math.log(rational, 2)))

    # find written duration
    written_duration = Fraction(1, 2) ** exponent

    # return written duration
    return written_duration
