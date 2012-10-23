from abjad.tools import mathtools


def integer_to_implied_prolation(n):
    '''.. versionadded:: 1.1

    Change positive integer `n` to implied porlation multiplier::

        >>> for denominator in range(1, 17):
        ...     multiplier = durationtools.integer_to_implied_prolation(denominator)
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

    Return multiplier less than or equal to ``1``.
    '''
    from abjad.tools import durationtools

    return durationtools.Multiplier(mathtools.greatest_power_of_two_less_equal(n), n)
