from abjad.tools.mathtools.divisors import divisors


def greatest_common_divisor(*integers):
    '''.. versionadded:: 2.0

    Greatest common divisor of `integers`::

        abjad> from abjad.tools import mathtools

    ::

        abjad> mathtools.greatest_common_divisor(84, -94, -144)
        2

    Allow nonpositive `integers`.

    Raise type error on noninteger `integers`.

    Raise not implemented error when ``0`` in `integers`.

    Return positive integer.
    '''

    common_divisors = None
    for positive_integer in integers:
        if not isinstance(positive_integer, int):
            raise TypeError('must be integer.')
        all_divisors = set(divisors(positive_integer))
        if common_divisors is None:
            common_divisors = all_divisors
        else:
            common_divisors &= all_divisors
            if common_divisors == set([1]):
                return 1
    return max(common_divisors)
