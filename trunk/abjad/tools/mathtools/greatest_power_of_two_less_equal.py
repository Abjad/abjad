from numbers import Number
import math


def greatest_power_of_two_less_equal(n, i = 0):
    r'''Greatest integer power of two less than or equal to positive `n`::

        abjad> from abjad.tools import mathtools

    ::

        abjad> for n in range(10, 20):
        ...     print '\t%s\t%s' % (n, mathtools.greatest_power_of_two_less_equal(n))
        ...
            10 8
            11 8
            12 8
            13 8
            14 8
            15 8
            16 16
            17 16
            18 16
            19 16

    Greatest-but-``i`` integer power of ``2`` less than or equal to positive `n`::

        abjad> for n in range(10, 20):
        ...     print '\t%s\t%s' % (n, mathtools.greatest_power_of_two_less_equal(n, i = 1))
        ...
            10 4
            11 4
            12 4
            13 4
            14 4
            15 4
            16 8
            17 8
            18 8
            19 8

    Raise type error on nonnumeric `n`.

    Raise value error on nonpositive `n`.

    Return positive integer.
    '''

    if not isinstance(n, Number):
        raise TypeError('"%s" must be number.' % str(n))

    if n <= 0:
        raise ValueError('"%s" must be positive.' % str(n))

    return 2 ** (int(math.log(n, 2)) - i)
