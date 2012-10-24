import fractions
from abjad.tools import mathtools


def multiply_duration_pair(pair, multiplier):
    '''.. versionadded:: 1.1

    Multiply duration `pair` by rational `multiplier`::

        >>> durationtools.multiply_duration_pair((4, 8), Fraction(4, 5))
        NonreducedFraction(16, 40)

    Naive multiplication with no simplification of anything intended 
    for certain types of meter multiplication.

    Return nonreduced fraction.

    .. versionchanged:: 2.0
        renamed ``durationtools.pair_multiply_naive()`` to
        ``durationtools.multiply_duration_pair()``.
    '''
    from abjad.tools import durationtools

#    assert isinstance(pair, tuple)
#    assert isinstance(multiplier, fractions.Fraction)
#
#    return pair[0] * multiplier.numerator, pair[1] * multiplier.denominator

    pair = mathtools.NonreducedFraction(pair)
    multiplier = mathtools.NonreducedFraction(multiplier)
    result = pair.multiply_without_reducing(multiplier)
    
    return result
