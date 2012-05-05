from abjad.tools import durationtools
from abjad.tools import mathtools
from abjad.tools.abctools.AbjadObject import AbjadObject
import fractions


class Pair(AbjadObject):
    r'''.. versionadded:: 2.9

    Pair of nonsimplifying integers::
        
        abjad> from abjad.tools import sequencetools

    ::

        abjad> sequencetools.Pair(3, 6)
        Pair(3, 6)

    Pairs implement addition and subtraction::

        abjad> sequencetools.Pair(3, 6) + sequencetools.Pair(3, 6)
        Pair(6, 6)

    Similar to built-in fraction except that numerator and denominator do not simplify.
    
    Useful when modeling certain operations on time signatures.

    Pairs are immutable.
    '''

    ### INITIALIZER ###

    def __init__(self, x, y):
        assert isinstance(x, int)
        assert mathtools.is_positive_integer(y)
        self.x = x
        self.y = y

    ### SPECIAL METHODS ###

    def __add__(self, expr):
        if isinstance(expr, type(self)):
            pass
        elif isinstance(expr, int):
            expr = type(self)(expr, 1)
        elif isinstance(expr, (fractions.Fraction, durationtools.Duration)):
            expr = type(self)(expr.numerator, expr.denominator)
        self_rational = fractions.Fraction(self.x, self.y)
        expr_rational = fractions.Fraction(expr.x, expr.y)
        result = self_rational + expr_rational
        lcm = mathtools.least_common_multiple(self.y, expr.y, result.denominator)
        result = durationtools.rational_to_duration_pair_with_specified_integer_denominator(result, lcm)
        result = type(self)(*result)
        return result
