from abjad.tools import mathtools
from fractions import Fraction


# TODO: respell function name correctly
def positive_integer_to_implied_prolation_multipler(n):
    '''.. versionadded:: 1.1

    Change positive integer `n` to implied porlation multiplier::

        abjad> from abjad.tools import durationtools

    ::

        abjad> for denominator in range(1, 17): # doctest: +SKIP
        ...     multiplier = durationtools.positive_integer_to_implied_prolation_multipler(denominator)
        ...     print '%s\\t%s' % (denominator, multiplier)
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
        ``durationtools.positive_integer_to_implied_prolation_multipler()``.
    '''

    return Fraction(mathtools.greatest_power_of_two_less_equal(n), n)
