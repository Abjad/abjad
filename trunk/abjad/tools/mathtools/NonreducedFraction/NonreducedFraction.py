from abjad.tools.abctools.AbjadObject import AbjadObject
from fractions import Fraction


class NonreducedFraction(AbjadObject):
    r'''.. versionadded:: 2.9

    Initialize with an integer numerator and integer denominator::
        
        abjad> from abjad.tools import sequencetools

    ::

        abjad> sequencetools.NonreducedFraction(3, 6)
        NonreducedFraction(3, 6)

    Or with only an integer denominator::

        abjad> sequencetools.NonreducedFraction(3)
        NonreducedFraction(3, 1)

    Or with an integer pair::

        abjad> sequencetools.NonreducedFraction((3, 6))
        NonreducedFraction(3, 6)

    Or with an integer singleton::

        abjad> sequencetools.NonreducedFraction((3,))
        NonreducedFraction(3, 1)
        
    Similar to built-in fraction except that numerator and denominator do not reduce.
    
    Nonreduced fractions are immutable.
    '''

    ### CLASS ATTRIBUTES ###

    __slots__ = ('_numerator', '_denominator')

    ### INITIALIZER ###

    def __init__(self, *args):
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
        self._numerator = numerator
        self._denominator = denominator

    ### SPECIAL METHODS ###

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

    def __ne__(self):
        '''True when `expr` does not equal `self`::
            
            abjad> mathtools.NonreducedFraction(3, 3) != 'foo'
            True

        Return boolean.
        '''
        return not self == expr

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
