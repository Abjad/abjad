import fractions
from abjad.tools import mathtools


def positive_integer_to_implied_prolation_multiplier(n):
    '''.. versionadded:: 1.1

    Change positive integer `n` to implied porlation multiplier::

        >>> for denominator in range(1, 17):
        ...     multiplier = durationtools.positive_integer_to_implied_prolation_multiplier(
        ...         denominator)
        ...     print '%s %4s' % (denominator, multiplier)
        ...
        1         1
        2         1
        3         2/3
        4         1
        5         4/5
        6         2/3
        7         4/7
        8         1
        9         8/9
        10        4/5
        11        8/11
        12        2/3
        13        8/13
        14        4/7
        15        8/15
        16        1

    Return positive fraction less than or equal to ``1``.

    .. versionchanged:: 2.0
        renamed ``durationtools.denominator_to_multiplier()`` to
        ``durationtools.positive_integer_to_implied_prolation_multiplier()``.
    '''

    return fractions.Fraction(mathtools.greatest_power_of_two_less_equal(n), n)
