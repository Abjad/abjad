#from abjad.tools.abctools.AbjadObject import AbjadObject
from abjad.tools.abctools.ImmutableAbjadObject import ImmutableAbjadObject
from fractions import Fraction


#class NonreducedFraction(AbjadObject):
class NonreducedFraction(ImmutableAbjadObject, Fraction):
    r'''.. versionadded:: 2.9

    Initialize with an integer numerator and integer denominator::
        
        abjad> from abjad.tools import mathtools

    ::

        abjad> mathtools.NonreducedFraction(3, 6)
        NonreducedFraction(3, 6)

    Initialize with only an integer denominator::

        abjad> mathtools.NonreducedFraction(3)
        NonreducedFraction(3, 1)

    Initialize with an integer pair::

        abjad> mathtools.NonreducedFraction((3, 6))
        NonreducedFraction(3, 6)

    Initialize with an integer singleton::

        abjad> mathtools.NonreducedFraction((3,))
        NonreducedFraction(3, 1)
        
    Similar to built-in fraction except that numerator and denominator do not reduce.

    Nonreduced fractions inherit from built-in fraction::

        abjad> isinstance(mathtools.NonreducedFraction(3, 6), Fraction)
        True

    Nonreduced fractions are numbers::

        abjad> import numbers

    ::

        abjad> isinstance(mathtools.NonreducedFraction(3, 6), numbers.Number)
        True
    
    Nonreduced fractions are immutable.
    '''

    ### CLASS ATTRIBUTES ###

    __slots__ = ('_numerator', '_denominator')

    ### INITIALIZER ###

    #def __init__(self, *args):
    def __new__(klass, *args):
        from abjad.tools import mathtools
        from abjad.tools import sequencetools
        if len(args) == 1 and hasattr(args[0], 'numerator') and hasattr(args[0], 'denominator'):
            numerator = args[0].numerator
            denominator = args[0].denominator
        elif len(args) == 1 and isinstance(args[0], int):
            numerator = args[0]
            denominator = 1
        elif len(args) == 1 and sequencetools.is_integer_singleton(args[0]):
            numerator = args[0][0]
            denominator = 1
        elif sequencetools.is_integer_pair(args):
            numerator = args[0]
            denominator = args[1]
        else:
            raise ValueError('can not initialize {} from {!r}.'.format(type(self).__class__.__name__, args))
        numerator *= mathtools.sign(denominator)
        denominator = abs(denominator)
        #self._numerator = numerator
        #self._denominator = denominator
        self = Fraction.__new__(klass, numerator, denominator)
        self._numerator = numerator
        self._denominator = denominator
        return self

    ### SPECIAL METHODS ###

    def __abs__(self):
        '''Absolute value of nonreduced fraction::

            abjad> abs(mathtools.NonreducedFraction(-3, 3))
            NonreducedFraction(3, 3)

        Return nonreduced fraction.
        '''
        return type(self)(abs(self.numerator), self.denominator)
        
    def __add__(self, expr):
        '''Add `expr` to `self`::

            abjad> mathtools.NonreducedFraction(3, 3) + 1
            NonreducedFraction(6, 3)

        Return nonreduced fraction.
        '''
        if isinstance(expr, type(self)):
            expr = expr.reduce()
        fraction = self.reduce() + expr
        return self._fraction_with_my_denominator(fraction)

    def __eq__(self, expr):
        '''True when `expr` equals `self`::

            abjad> mathtools.NonreducedFraction(3, 3) == 1
            True
    
        Return boolean.
        '''
        return self.reduce() == expr

    def __ge__(self, expr):
        '''True when nonreduced fraction is greater than or equal to `expr`::

            abjad> mathtools.NonreducedFraction(3, 3) >= 1
            True
            
        Return boolean.
        '''
        return self.reduce() >= expr

    def __gt__(self, expr):
        '''True when nonreduced fraction is greater than `expr`::

            abjad> mathtools.NonreducedFraction(3, 3) > 1
            False
            
        Return boolean.
        '''
        return self.reduce() > expr

    def __le__(self, expr):
        '''True when nonreduced fraction is less than or equal to `expr`::

            abjad> mathtools.NonreducedFraction(3, 3) <= 1
            True
            
        Return boolean.
        '''
        return self.reduce() <= expr

    def __lt__(self, expr):
        '''True when nonreduced fraction is less than `expr`::

            abjad> mathtools.NonreducedFraction(3, 3) < 1
            False

        Return boolean.
        '''
        return self.reduce() < expr

    def __mul__(self, expr):
        '''Multiply reduced fraction by expr::

            abjad> mathtools.NonreducedFraction(3, 3) * 3
            NonreducedFraction(9, 3)

        Return reduced fraction.
        '''
        if isinstance(expr, type(self)):
            expr = expr.reduce()
        fraction = self.reduce() * expr
        return self._fraction_with_my_denominator(fraction)

    def __ne__(self):
        '''True when `expr` does not equal `self`::
            
            abjad> mathtools.NonreducedFraction(3, 3) != 'foo'
            True

        Return boolean.
        '''
        return not self == expr

    def __neg__(self):
        '''Negate nonreduced fraction::

            abjad> -mathtools.NonreducedFraction(3, 3)
            NonreducedFraction(-3, 3)

        Return nonreduced fraction.
        '''
        return type(self)(-self.numerator, self.denominator)

    def __radd__(self, expr):
        '''Add nonreduced fraction to `expr`::

            abjad> 1 + mathtools.NonreducedFraction(3, 3)
            NonreducedFraction(6, 3)

        Return nonreduced fraction.
        '''
        return self + expr

    def __rmul__(self, expr):
        '''Multiply expr by reduced fraction::

            abjad> 3 * mathtools.NonreducedFraction(3, 3)
            NonreducedFraction(9, 3)

        Return reduced fraction.
        '''
        return self * expr

    def __rsub__(self, expr):
        '''Subtract nonreduced fraction from `expr`::

            abjad> 1 - mathtools.NonreducedFraction(3, 3)
            NonreducedFraction(0, 3)

        Return nonreduced fraction.
        '''
        return -self + expr

    def __str__(self):
        '''String representation of nonreduced fraction::

            abjad> fraction = mathtools.NonreducedFraction(-6, 3)
    
        ::

            abjad> str(fraction)
            '-6/3'
        
        Return string.
        '''
        return '{}/{}'.format(self.numerator, self.denominator)

    def __sub__(self, expr):
        '''Subtract `expr` from self::

            abjad> mathtools.NonreducedFraction(3, 3) - 2
            NonreducedFraction(-3, 3)

        Return nonreduced fraction.
        '''
        if isinstance(expr, type(self)):
            expr = expr.reduce()
        fraction = self.reduce() - expr
        return self._fraction_with_my_denominator(fraction)

    ### READ-ONLY PRIVATE PROPERTIES ###

    @property
    def _mandatory_argument_values(self):
        return self.numerator, self.denominator

    ### PRIVATE METHODS ###

    def _fraction_with_my_denominator(self, fraction):
        from abjad.tools import durationtools
        from abjad.tools import mathtools
        denominator = mathtools.least_common_multiple(self.denominator, fraction.denominator)
        pair = durationtools.rational_to_duration_pair_with_specified_integer_denominator(fraction, denominator)
        return type(self)(*pair)

    ### READ-ONLY PUBLIC PROPERTIES ###

    @property
    def denominator(self):
        '''Read-only denominator of nonreduced fraction::

            abjad> fraction = mathtools.NonreducedFraction(-6, 3)

        ::

            abajd> fraction.denominator
            3

        Return positive integer.
        '''
        return self._denominator

    @property
    def numerator(self):
        '''Read-only numerator of nonreduced fraction::

            abjad> fraction = mathtools.NonreducedFraction(-6, 3)

        ::

            abajd> fraction.numerator
            3

        Return integer.
        '''
        return self._numerator

    @property
    def pair(self):
        '''Read only pair of nonreduced fraction numerator and denominator::

            abjad> fraction = mathtools.NonreducedFraction(-6, 3)

        ::

            abjad> fraction.pair
            (-6, 3)

        Return integer pair.
        '''
        return self.numerator, self.denominator

    ### PUBLIC METHODS ###

    def reduce(self):
        '''Reduce nonreduced fraction::

            abjad> fraction = mathtools.NonreducedFraction(-6, 3)

        ::

            abjad> fraction.reduce()
            Fraction(-2, 1)
            
        Return fraction.
        '''
        return Fraction(self.numerator, self.denominator)
