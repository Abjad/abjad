from numbers import Number
import math


def greatest_multiple_less_equal(m, n):
    '''Greatest integer multiple of `m` less than or equal to `n`::

        abjad> from abjad.tools import mathtools

    ::

        abjad> mathtools.greatest_multiple_less_equal(10, 47)
        40

    ::

        abjad> for m in range(1, 10):
        ...     print m, mathtools.greatest_multiple_less_equal(m, 47)
        ...
        1 47
        2 46
        3 45
        4 44
        5 45
        6 42
        7 42
        8 40
        9 45

    ::

        abjad> for n in range(10, 100, 10):
        ...     print mathtools.greatest_multiple_less_equal(7, n), n
        ...
        7 10
        14 20
        28 30
        35 40
        49 50
        56 60
        70 70
        77 80
        84 90

    Raise type error on nonnumeric `m`.

    Raise type error on nonnumeric `n`.

    Return nonnegative integer.
    '''

    if not isinstance(m, Number):
        raise TypeError('"%s" must be number.' % str(m))

    if not isinstance(n, Number):
        raise TypeError('"%s" must be number.' % str(n))

    return m * int(math.floor(n / float(m)))
