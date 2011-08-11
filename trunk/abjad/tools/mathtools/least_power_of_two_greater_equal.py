from fractions import Fraction
import math


def least_power_of_two_greater_equal(n, i = 0):
    r'''Return least integer power of two greater than or equal to positive `n`::

        abjad> from abjad.tools import mathtools

    ::

        abjad> for n in range(10, 20):
        ...     print '\t%s\t%s' % (n, mathtools.least_power_of_two_greater_equal(n))
        ...
            10 16
            11 16
            12 16
            13 16
            14 16
            15 16
            16 16
            17 32
            18 32
            19 32

    When ``i = 1``, return the first integer power of ``2`` greater than
    the least integer power of ``2`` greater than or equal to *n*.

    ::

        abjad> for n in range(10, 20):
        ...     print '\t%s\t%s' % (n, mathtools.least_power_of_two_greater_equal(n, i = 1))
        ...
            10 32
            11 32
            12 32
            13 32
            14 32
            15 32
            16 32
            17 64
            18 64
            19 64

    When ``i = 2``, return the second integer power of ``2`` greater than
    the least integer power of ``2`` greater than or equal to `n`, and,
    in general, return the ``i`` th integer power of ``2`` greater than
    the least integer power of ``2`` greater than or equal to `n`.

    Raise type error on nonnumeric `n`.

    Raise value error on nonpositive `n`.

    Return integer.
    '''

    if not isinstance(n, (int, long, float, Fraction)):
        raise TypeError

    if n <= 0:
        raise ValueError

    return 2 ** (int(math.ceil(math.log(n, 2))) + i)
