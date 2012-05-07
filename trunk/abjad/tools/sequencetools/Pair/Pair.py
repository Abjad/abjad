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

    def __init__(self, *args):
        from abjad.tools import sequencetools
        if len(args) == 1 and hasattr(args[0], 'numerator') and hasattr(args[0], 'denominator'):
            self.numerator = args[0].numerator
            self.denominator = args[0].denominator
        elif len(args) == 1 and isinstance(args[0], int):
            self.numerator = args[0]
            self.denominator = 1
        elif len(args) == 1 and sequencetools.is_integer_singleton(args[0]):
            self.numerator = args[0][0]
            self.denominator = 1
        elif sequencetools.is_integer_pair(args):
            self.numerator = args[0]
            self.denominator = args[1]
        else:
            raise ValueError('can not initialize pair from {!r}.'.format(args))
        self.numerator *= mathtools.sign(self.denominator)

    ### SPECIAL METHODS ###

    def __add__(self, expr):
        if isinstance(expr, type(self)):
            pass
        elif isinstance(expr, int):
            expr = type(self)(expr, 1)
        elif isinstance(expr, (fractions.Fraction, durationtools.Duration)):
            expr = type(self)(expr.numerator, expr.denominator)
        self_rational = fractions.Fraction(self.numerator, self.denominator)
        expr_rational = fractions.Fraction(expr.numerator, expr.denominator)
        result = self_rational + expr_rational
        lcm = mathtools.least_common_multiple(self.numerator, expr.denominator, result.denominator)
        result = durationtools.rational_to_duration_pair_with_specified_integer_denominator(result, lcm)
        result = type(self)(*result)
        return result

    def __sub__(self, expr):
        pass

    ### READ-ONLY PRIVATE PROPERTIES ###

    @property
    def _mandatory_argument_values(self):
        return self.numerator, self.denominator

    ### PRIVATE METHODS ###

    def _coerce(self):
        pass
