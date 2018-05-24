def integer_to_binary_string(n):
    r"""
    Changes positive integer ``n`` to binary string.

    ..  container:: example

        >>> for n in range(1, 16 + 1):
        ...     print('{}\t{}'.format(n, abjad.mathtools.integer_to_binary_string(n)))
        ...
        1  1
        2  10
        3  11
        4  100
        5  101
        6  110
        7  111
        8  1000
        9  1001
        10 1010
        11 1011
        12 1100
        13 1101
        14 1110
        15 1111
        16 10000

    Returns string.
    """
    if n == 0:
        return '0'
    result = bin(abs(n)).lstrip('-0b')
    if n < 0:
        result = '-' + result
    return result
