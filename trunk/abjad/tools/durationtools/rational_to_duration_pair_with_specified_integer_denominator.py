from abjad.tools.durationtools.duration_token_to_duration_pair import duration_token_to_duration_pair
from fractions import Fraction


def rational_to_duration_pair_with_specified_integer_denominator(duration, integer_denominator):
    r'''.. versionadded:: 1.1

    Change `duration` to duraiton pair with specified `integer_denominator`::

        abjad> from abjad.tools import durationtools

    ::

        abjad> for n in range(1, 17):
        ...     rational = Fraction(n, 16)
        ...     pair = durationtools.rational_to_duration_pair_with_specified_integer_denominator(rational, 16)
        ...     print '%s\t%s' % (rational, pair)
        ...
        1/16    (1, 16)
        1/8     (2, 16)
        3/16    (3, 16)
        1/4     (4, 16)
        5/16    (5, 16)
        3/8     (6, 16)
        7/16    (7, 16)
        1/2     (8, 16)
        9/16    (9, 16)
        5/8     (10, 16)
        11/16   (11, 16)
        3/4     (12, 16)
        13/16   (13, 16)
        7/8     (14, 16)
        15/16   (15, 16)
        1         (16, 16)

    Return integer pair.

    .. versionchanged:: 2.0
        renamed ``durationtools.in_terms_of()`` to
        ``durationtools.rational_to_duration_pair_with_specified_integer_denominator()``.
    '''

    assert isinstance(duration, (Fraction, int, long, tuple))
    n, d = duration_token_to_duration_pair(duration)
    multiplier = Fraction(integer_denominator, d)
    new_numerator = multiplier * n
    new_denominator = multiplier * d
    if new_numerator.denominator == 1 and new_denominator.denominator == 1:
        return (new_numerator.numerator, new_denominator.numerator)
    else:
        return (n, d)
