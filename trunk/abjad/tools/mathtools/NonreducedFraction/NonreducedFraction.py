import fractions
from abjad.tools.abctools.ImmutableAbjadObject import ImmutableAbjadObject


class NonreducedFraction(ImmutableAbjadObject, fractions.Fraction):
    r'''.. versionadded:: 2.9

    Initialize with an integer numerator and integer denominator:

    ::

        >>> mathtools.NonreducedFraction(3, 6)
        NonreducedFraction(3, 6)

    Initialize with only an integer denominator:

    ::

        >>> mathtools.NonreducedFraction(3)
        NonreducedFraction(3, 1)

    Initialize with an integer pair:

    ::

        >>> mathtools.NonreducedFraction((3, 6))
        NonreducedFraction(3, 6)

    Initialize with an integer singleton:

    ::

        >>> mathtools.NonreducedFraction((3,))
        NonreducedFraction(3, 1)

    Similar to built-in fraction except that numerator and denominator do not reduce.

    Nonreduced fractions inherit from built-in fraction:

    ::

        >>> isinstance(mathtools.NonreducedFraction(3, 6), Fraction)
        True

    Nonreduced fractions are numbers:

    ::

        >>> import numbers

    ::

        >>> isinstance(mathtools.NonreducedFraction(3, 6), numbers.Number)
        True

    Nonreduced fraction initialization requires more function calls that fraction initialization.
    But nonreduced fraction initialization is reasonably fast anyway:

    ::

        >>> import fractions
        >>> iotools.count_function_calls('fractions.Fraction(3, 6)', globals())
        13

    ::

        >>> iotools.count_function_calls('mathtools.NonreducedFraction(3, 6)', globals())
        28

    Nonreduced fractions are immutable.
    '''

    ### CLASS ATTRIBUTES ###

    __slots__ = ('_numerator', '_denominator')

    ### INITIALIZER ###

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
        elif len(args) == 1 and sequencetools.is_integer_pair(args[0]):
            numerator, denominator = args[0]
        elif sequencetools.is_integer_pair(args):
            numerator = args[0]
            denominator = args[1]
        else:
            raise ValueError('can not initialize NonreducedFraction from {!r}.'.format(args))
        numerator *= mathtools.sign(denominator)
        denominator = abs(denominator)
        self = fractions.Fraction.__new__(klass, numerator, denominator)
        self._numerator = numerator
        self._denominator = denominator
        return self

    ### SPECIAL METHODS ###

    def __abs__(self):
        '''Absolute value of nonreduced fraction:

        ::

            >>> abs(mathtools.NonreducedFraction(-3, 3))
            NonreducedFraction(3, 3)

        Return nonreduced fraction.
        '''
        return type(self)((abs(self.numerator), self.denominator))

    def __add__(self, expr):
        '''Add `expr` to nonreduced fraction:

        ::

            >>> mathtools.NonreducedFraction(3, 3) + 1
            NonreducedFraction(6, 3)

        Adding two nonreduced fractions is fairly fast:

        ::

            >>> a = mathtools.NonreducedFraction(3, 6)
            >>> b = mathtools.NonreducedFraction(3, 12)
            >>> iotools.count_function_calls('a + b', globals())
            65

        Adding an integer is even faster:

        ::

            >>> iotools.count_function_calls('a + 10', globals())
            33

        Return nonreduced fraction.
        '''
        from abjad.tools import mathtools
        if isinstance(expr, int):
            numerator = self.numerator + expr * self.denominator
            return NonreducedFraction(numerator, self.denominator)
        elif hasattr(expr, 'denominator'):
            if self.denominator == expr.denominator:
                numerator = self.numerator + expr.numerator
                return NonreducedFraction(numerator, self.denominator)
            else:
                denominator = mathtools.least_common_multiple(self.denominator, expr.denominator)
                self_multiplier = denominator / self.denominator
                expr_multiplier = denominator / expr.denominator
                self_numerator = self_multiplier * self.numerator
                expr_numerator = expr_multiplier * expr.numerator
                return NonreducedFraction(self_numerator + expr_numerator, denominator)
        else:
            raise ValueError(expr)

    def __div__(self, expr):
        '''Divide nonreduced fraction by expr:

        ::

            >>> mathtools.NonreducedFraction(3, 3) / 1
            NonreducedFraction(3, 3)

        Return nonreduced fraction.
        '''
        denominators = [self.denominator]
        if isinstance(expr, type(self)):
            denominators.append(expr.denominator)
            expr = expr.reduce()
        fraction = self.reduce() / expr
        return self._fraction_with_denominator(fraction, max(denominators))

    def __eq__(self, expr):
        '''True when `expr` equals `self`:

        ::

            >>> mathtools.NonreducedFraction(3, 3) == 1
            True

        Return boolean.
        '''
        return self.reduce() == expr

    def __ge__(self, expr):
        '''True when nonreduced fraction is greater than or equal to `expr`:

        ::

            >>> mathtools.NonreducedFraction(3, 3) >= 1
            True

        Return boolean.
        '''
        return self.reduce() >= expr

    def __gt__(self, expr):
        '''True when nonreduced fraction is greater than `expr`:

        ::

            >>> mathtools.NonreducedFraction(3, 3) > 1
            False

        Return boolean.
        '''
        return self.reduce() > expr

    def __le__(self, expr):
        '''True when nonreduced fraction is less than or equal to `expr`:

        ::

            >>> mathtools.NonreducedFraction(3, 3) <= 1
            True

        Return boolean.
        '''
        return self.reduce() <= expr

    def __lt__(self, expr):
        '''True when nonreduced fraction is less than `expr`:

        ::

            >>> mathtools.NonreducedFraction(3, 3) < 1
            False

        Return boolean.
        '''
        return self.reduce() < expr

    def __mul__(self, expr):
        '''Multiply nonreduced fraction by expr:

        ::

            >>> mathtools.NonreducedFraction(3, 3) * 3
            NonreducedFraction(9, 3)

        Return nonreduced fraction.
        '''
        denominators = [self.denominator]
        if isinstance(expr, type(self)):
            denominators.append(expr.denominator)
            expr = expr.reduce()
        fraction = self.reduce() * expr
        return self._fraction_with_denominator(fraction, max(denominators))

    def __ne__(self, expr):
        '''True when `expr` does not equal `self`:

        ::

            >>> mathtools.NonreducedFraction(3, 3) != 'foo'
            True

        Return boolean.
        '''
        return not self == expr

    def __neg__(self):
        '''Negate nonreduced fraction:

        ::

            >>> -mathtools.NonreducedFraction(3, 3)
            NonreducedFraction(-3, 3)

        Return nonreduced fraction.
        '''
        return type(self)((-self.numerator, self.denominator))

    def __radd__(self, expr):
        '''Add nonreduced fraction to `expr`:

        ::

            >>> 1 + mathtools.NonreducedFraction(3, 3)
            NonreducedFraction(6, 3)

        Return nonreduced fraction.
        '''
        return self + expr

    def __rdiv__(self, expr):
        '''Divide `expr` by nonreduced fraction:

        ::

            >>> 1 / mathtools.NonreducedFraction(3, 3)
            NonreducedFraction(3, 3)

        Return nonreduced fraction.
        '''
        denominators = [self.denominator]
        if isinstance(expr, type(self)):
            denominators.append(expr.denominator)
            expr = expr.reduce()
        fraction = expr / self.reduce()
        return self._fraction_with_denominator(fraction, max(denominators))

    def __rmul__(self, expr):
        '''Multiply `expr` by nonreduced fraction:

        ::

            >>> 3 * mathtools.NonreducedFraction(3, 3)
            NonreducedFraction(9, 3)

        Return nonreduced fraction.
        '''
        return self * expr

    def __rsub__(self, expr):
        '''Subtract nonreduced fraction from `expr`:

        ::

            >>> 1 - mathtools.NonreducedFraction(3, 3)
            NonreducedFraction(0, 3)

        Return nonreduced fraction.
        '''
        return -self + expr

    def __str__(self):
        '''String representation of nonreduced fraction:

        ::

            >>> fraction = mathtools.NonreducedFraction(-6, 3)

        ::

            >>> str(fraction)
            '-6/3'

        Return string.
        '''
        return '{}/{}'.format(self.numerator, self.denominator)

    def __sub__(self, expr):
        '''Subtract `expr` from self:

        ::

            >>> mathtools.NonreducedFraction(3, 3) - 2
            NonreducedFraction(-3, 3)

        Return nonreduced fraction.
        '''
        denominators = [self.denominator]
        if isinstance(expr, type(self)):
            denominators.append(expr.denominator)
            expr = expr.reduce()
        fraction = self.reduce() - expr
        return self._fraction_with_denominator(fraction, max(denominators))

    ### READ-ONLY PRIVATE PROPERTIES ###

    @property
    def _positional_argument_values(self):
        return self.numerator, self.denominator

    ### PRIVATE METHODS ###

    def _fraction_with_denominator(self, fraction, denominator):
        from abjad.tools import durationtools
        from abjad.tools import mathtools
        denominator = mathtools.least_common_multiple(denominator, fraction.denominator)
        return NonreducedFraction(fraction).with_denominator(denominator)

    # do not indent in storage
    def _get_tools_package_qualified_repr_pieces(self, is_indented=True):
        return [''.join(
            ImmutableAbjadObject._get_tools_package_qualified_repr_pieces(self, is_indented=False))]

    ### READ-ONLY PUBLIC PROPERTIES ###

    @property
    def denominator(self):
        '''Read-only denominator of nonreduced fraction:

        ::

            >>> fraction = mathtools.NonreducedFraction(-6, 3)

        ::

            >>> fraction.denominator
            3

        Return positive integer.
        '''
        return self._denominator

    @property
    def imag(self):
        '''Nonreduced fractions have no imaginary part:

        ::

            >>> fraction.imag
            0

        Return zero.
        '''
        return Fraction.imag.fget(self)

    @property
    def numerator(self):
        '''Read-only numerator of nonreduced fraction:

        ::

            >>> fraction = mathtools.NonreducedFraction(-6, 3)

        ::

            >>> fraction.numerator
            -6

        Return integer.
        '''
        return self._numerator

    @property
    def pair(self):
        '''Read only pair of nonreduced fraction numerator and denominator:

        ::

            >>> fraction = mathtools.NonreducedFraction(-6, 3)

        ::

            >>> fraction.pair
            (-6, 3)

        Return integer pair.
        '''
        return self.numerator, self.denominator

    @property
    def real(self):
        '''Nonreduced fractions are their own real component:

        ::

            >>> fraction.real
            NonreducedFraction(-6, 3)

        Return nonreduced fraction.
        '''
        return self

    @property
    def storage_format(self):
        '''Nonreduced fraction storage format:

        ::

            >>> z(fraction)
            mathtools.NonreducedFraction(-6, 3)

        Return string.
        '''
        return AbjadObject.storage_format.fget(self)

    ### PUBLIC METHODS ###

    def multiply_with_cross_cancelation(self, multiplier):
        '''.. versionadded:: 2.11

        Multiply nonreduced fraction by `expr` with cross-cancelation:

        ::

            >>> mathtools.NonreducedFraction(4, 8).multiply_with_cross_cancelation((2, 3))
            NonreducedFraction(4, 12)

        ::

            >>> mathtools.NonreducedFraction(4, 8).multiply_with_cross_cancelation((4, 1))
            NonreducedFraction(4, 2)

        ::

            >>> mathtools.NonreducedFraction(4, 8).multiply_with_cross_cancelation((3, 5))
            NonreducedFraction(12, 40)

        ::

            >>> mathtools.NonreducedFraction(4, 8).multiply_with_cross_cancelation((6, 5))
            NonreducedFraction(12, 20)

        ::

            >>> mathtools.NonreducedFraction(5, 6).multiply_with_cross_cancelation((6, 5))
            NonreducedFraction(1, 1)

        Return nonreduced fraction.
        '''
        from abjad.tools import durationtools
        from abjad.tools import mathtools

        multiplier = durationtools.Multiplier(multiplier)

        self_numerator_factors = mathtools.factors(self.numerator)
        multiplier_denominator_factors = mathtools.factors(multiplier.denominator)
        for factor in multiplier_denominator_factors[:]:
            if factor in self_numerator_factors:
                self_numerator_factors.remove(factor)
                multiplier_denominator_factors.remove(factor)

        self_denominator_factors = mathtools.factors(self.denominator)
        multiplier_numerator_factors = mathtools.factors(multiplier.numerator)
        for factor in multiplier_numerator_factors[:]:
            if factor in self_denominator_factors:
                self_denominator_factors.remove(factor)
                multiplier_numerator_factors.remove(factor)

        result_numerator_factors = self_numerator_factors + \
            multiplier_numerator_factors
        result_denominator_factors = self_denominator_factors + \
            multiplier_denominator_factors

        result_numerator = 1
        for factor in result_numerator_factors:
            result_numerator *= factor

        result_denominator = 1
        for factor in result_denominator_factors:
            result_denominator *= factor

        return NonreducedFraction(result_numerator, result_denominator)

    def multiply_with_numerator_preservation(self, multiplier):
        '''Multiply nonreduced fraction by `multiplier` with numerator preservation
        where possible:

        ::

            >>> mathtools.NonreducedFraction(9, 16).multiply_with_numerator_preservation((2, 3))
            NonreducedFraction(9, 24)

        ::

            >>> mathtools.NonreducedFraction(9, 16).multiply_with_numerator_preservation((1, 2))
            NonreducedFraction(9, 32)

        ::

            >>> mathtools.NonreducedFraction(9, 16).multiply_with_numerator_preservation((5, 6))
            NonreducedFraction(45, 96)

        ::

            >>> mathtools.NonreducedFraction(3, 8).multiply_with_numerator_preservation((2, 3))
            NonreducedFraction(3, 12)

        Return nonreduced fraction.
        '''
        from abjad.tools import durationtools

        multiplier = durationtools.Multiplier(multiplier)
        self_denominator = self.denominator
        candidate_result_denominator = self_denominator / multiplier

        if candidate_result_denominator.denominator == 1:
            return NonreducedFraction(self.numerator, candidate_result_denominator.numerator)
        else:
            result_numerator = self.numerator * candidate_result_denominator.denominator
            result_denominator = candidate_result_denominator.numerator
            return NonreducedFraction(result_numerator, result_denominator)

    def multiply_without_reducing(self, expr):
        '''Multiply nonreduced fraction by `expr` without reducing:

        ::

            >>> mathtools.NonreducedFraction(3, 8).multiply_without_reducing((3, 3))
            NonreducedFraction(9, 24)

        ::

            >>> mathtools.NonreducedFraction(4, 8).multiply_without_reducing((4, 5))
            NonreducedFraction(16, 40)

        ::

            >>> mathtools.NonreducedFraction(4, 8).multiply_without_reducing((3, 4))
            NonreducedFraction(12, 32)

        Return nonreduced fraction.
        '''
        expr = NonreducedFraction(expr)
        numerator = self.numerator * expr.numerator
        denominator = self.denominator * expr.denominator
        return NonreducedFraction(numerator, denominator)

    def reduce(self):
        '''Reduce nonreduced fraction:

        ::

            >>> fraction = mathtools.NonreducedFraction(-6, 3)

        ::

            >>> fraction.reduce()
            Fraction(-2, 1)

        Return fraction.
        '''
        return fractions.Fraction(self.numerator, self.denominator)

    def with_denominator(self, denominator):
        '''Return new nonreduced fraction with integer `denominator`:

        ::

            >>> mathtools.NonreducedFraction(3, 6).with_denominator(12)
            NonreducedFraction(6, 12)

        Return nonreduced fraction.
        '''
        from abjad.tools import durationtools
        n, d = self.pair
        multiplier = durationtools.Multiplier(denominator, d)
        new_numerator = multiplier * n
        new_denominator = multiplier * d
        if new_numerator.denominator == 1 and new_denominator.denominator == 1:
            return type(self)(new_numerator.numerator, new_denominator.numerator)
        else:
            return type(self)(n, d)

    def with_multiple_of_denominator(self, denominator):
        '''Return new nonreduced fraction with multiple of integer `denominator`:

        ::

            >>> mathtools.NonreducedFraction(3, 6).with_multiple_of_denominator(5)
            NonreducedFraction(5, 10)

        Return nonreduced fraction.
        '''
        result = self.with_denominator(denominator)
        while not result.denominator == denominator:
            denominator *= 2
            result = result.with_denominator(denominator)
        return result
