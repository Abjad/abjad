import math


def binomial_coefficient(n, k):
    """
    Gets binomial coefficient of ``n`` choose ``k``.

    ..  container:: example

        >>> for k in range(8):
        ...     print(k, '\t', abjad.mathtools.binomial_coefficient(8, k))
        ...
        0  1
        1  8
        2  28
        3  56
        4  70
        5  56
        6  28
        7  8

    Returns positive integer.
    """
    return math.factorial(n) // (math.factorial(n - k) * math.factorial(k))
