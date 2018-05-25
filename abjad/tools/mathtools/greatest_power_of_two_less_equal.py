import math
import numbers


def greatest_power_of_two_less_equal(n, i=0):
    r"""
    Gets greatest integer power of two less than or equal to positive ``n``.

    ..  container:: example

        >>> for n in range(10, 20):
        ...     print('\t%s\t%s' % (n, abjad.mathtools.greatest_power_of_two_less_equal(n)))
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

        Greatest-but-``i`` integer power of ``2`` less than or equal to
        positive ``n``:

        >>> for n in range(10, 20):
        ...     print('\t%s\t%s' % (n, abjad.mathtools.greatest_power_of_two_less_equal(n, i=1)))
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

    Returns positive integer.
    """
    if not isinstance(n, numbers.Number):
        message = 'must be number: {!r}.'
        message = message.format(n)
        raise TypeError(message)
    if n <= 0:
        message = 'must be positive: {!r}.'
        message = message.format(n)
        raise ValueError(message)
    return 2 ** (int(math.log(n, 2)) - i)
