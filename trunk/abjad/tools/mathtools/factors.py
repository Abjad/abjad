from abjad.tools.mathtools.is_positive_integer import is_positive_integer


def factors(n):
    '''Integer factors of positive integer `n` in increasing order::

        abjad> from abjad.tools import mathtools

    ::

        abjad> mathtools.factors(84)
        [1, 2, 2, 3, 7]

    ::

        abjad> for n in range(10, 20):
        ...   print n, mathtools.factors(n)
        ...
        10 [1, 2, 5]
        11 [1, 11]
        12 [1, 2, 2, 3]
        13 [1, 13]
        14 [1, 2, 7]
        15 [1, 3, 5]
        16 [1, 2, 2, 2, 2]
        17 [1, 17]
        18 [1, 2, 3, 3]
        19 [1, 19]

    Raise type error on noninteger `n`.

    Raise value error on nonpositive `n`.

    Return list of one or more positive integers.
    '''

    if not is_positive_integer(n):
        raise TypeError('"%s" must be positive integer.' % str(n))

    d = 2
    factors = [1]
    while 1 < n:
        if n % d == 0:
            factors.append(d)
            n = n/d
        else:
            d = d + 1
    return factors
