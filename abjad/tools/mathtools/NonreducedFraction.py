# -*- encoding: utf-8 -*-
import fractions
from abjad.tools.abctools.AbjadObject import AbjadObject


class NonreducedFraction(AbjadObject, fractions.Fraction):
    r'''Initializes with an integer numerator and integer denominator:

    ::

        >>> mathtools.NonreducedFraction(3, 6)
        NonreducedFraction(3, 6)

    Initializes with only an integer denominator:

    ::

        >>> mathtools.NonreducedFraction(3)
        NonreducedFraction(3, 1)

    Initializes with an integer pair:

    ::

        >>> mathtools.NonreducedFraction((3, 6))
        NonreducedFraction(3, 6)

    Initializes with an integer singleton:

    ::

        >>> mathtools.NonreducedFraction((3,))
        NonreducedFraction(3, 1)

    Similar to built-in fraction except that numerator and denominator
    do not reduce.

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

    '''

    ### CLASS VARIABLES ###

    __slots__ = ()

    ### CONSTRUCTOR ###

    def __new__(cls, *args):
        from abjad.tools import mathtools
        if len(args) == 1 and hasattr(args[0], 'numerator') and \
            hasattr(args[0], 'denominator'):
            numerator = args[0].numerator
            denominator = args[0].denominator
        elif len(args) == 1 and isinstance(args[0], int):
            numerator = args[0]
            denominator = 1
        elif len(args) == 1 and mathtools.is_integer_singleton(args[0]):
            numerator = args[0][0]
            denominator = 1
        elif len(args) == 1 and mathtools.is_integer_pair(args[0]):
            numerator, denominator = args[0]
        elif len(args) == 1 and isinstance(args[0], str):
            numerator, denominator = cls._parse_input_string(args[0])
        elif mathtools.is_integer_pair(args):
            numerator = args[0]
            denominator = args[1]
        elif len(args) == 0:
            numerator = 0
            denominator = 1
        else:
            message = 'can not initialize {}: {!r}.'
            message = message.format(cls.__name__, args)
            raise ValueError(message)
        numerator *= mathtools.sign(denominator)
        denominator = abs(denominator)
        self = fractions.Fraction.__new__(cls, numerator, denominator)
        self._numerator = numerator
        self._denominator = denominator
        return self

    ### SPECIAL METHODS ###

    def __abs__(self):
        r'''Absolute value of nonreduced fraction.

        ::

            >>> abs(mathtools.NonreducedFraction(-3, 3))
            NonreducedFraction(3, 3)

        Returns nonreduced fraction.
        '''
        return type(self)((abs(self.numerator), self.denominator))

    def __add__(self, expr):
        r'''Adds `expr` to nonreduced fraction.

        ::

            >>> mathtools.NonreducedFraction(3, 3) + 1
            NonreducedFraction(6, 3)

        Returns nonreduced fraction.
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
                denominator = mathtools.least_common_multiple(
                    self.denominator, expr.denominator)
                self_multiplier = denominator // self.denominator
                expr_multiplier = denominator // expr.denominator
                self_numerator = self_multiplier * self.numerator
                expr_numerator = expr_multiplier * expr.numerator
                return NonreducedFraction(
                    self_numerator + expr_numerator, denominator)
        else:
            raise ValueError(expr)

    def __div__(self, expr):
        r'''Divides nonreduced fraction by `expr`.

        ::

            >>> mathtools.NonreducedFraction(3, 3) / 1
            NonreducedFraction(3, 3)

        Returns nonreduced fraction.
        '''
        denominators = [self.denominator]
        if isinstance(expr, type(self)):
            denominators.append(expr.denominator)
            expr = expr.reduce()
        fraction = self.reduce() / expr
        return self._fraction_with_denominator(fraction, max(denominators))

    def __eq__(self, expr):
        r'''Is true when `expr` equals nonreduced fraction.

        ::

            >>> mathtools.NonreducedFraction(3, 3) == 1
            True

        Returns boolean.
        '''
        return self.reduce() == expr

    def __format__(self, format_specification=''):
        r'''Formats nonreduced fraction.

        Set `format_specification` to `''` or `'storage'`.
        Interprets `''` equal to `'storage'`.

        ::

            >>> fraction = mathtools.NonreducedFraction(-6, 3)
            >>> print(format(fraction))
            mathtools.NonreducedFraction(-6, 3)

        Returns string.
        '''
        from abjad.tools import systemtools
        if format_specification in ('', 'storage'):
            return systemtools.StorageFormatManager.get_storage_format(self)
        return str(self)

    def __ge__(self, expr):
        r'''Is true when nonreduced fraction is greater than or equal to `expr`.

        ::

            >>> mathtools.NonreducedFraction(3, 3) >= 1
            True

        Returns boolean.
        '''
        return self.reduce() >= expr

    def __gt__(self, expr):
        r'''Is true when nonreduced fraction is greater than `expr`.

        ::

            >>> mathtools.NonreducedFraction(3, 3) > 1
            False

        Returns boolean.
        '''
        return self.reduce() > expr

    def __hash__(self):
        r'''Hashes nonreduced fraction.

        Required to be explicitly re-defined on Python 3 if __eq__ changes.

        Returns integer.
        '''
        return super(NonreducedFraction, self).__hash__()

    def __le__(self, expr):
        r'''Is true when nonreduced fraction is less than or equal to `expr`.

        ::

            >>> mathtools.NonreducedFraction(3, 3) <= 1
            True

        Returns boolean.
        '''
        return self.reduce() <= expr

    def __lt__(self, expr):
        r'''Is true when nonreduced fraction is less than `expr`.

        ::

            >>> mathtools.NonreducedFraction(3, 3) < 1
            False

        Returns boolean.
        '''
        return self.reduce() < expr

    def __mul__(self, expr):
        r'''Multiplies nonreduced fraction by `expr`.

        ::

            >>> mathtools.NonreducedFraction(3, 3) * 3
            NonreducedFraction(9, 3)

        Returns nonreduced fraction.
        '''
        denominators = [self.denominator]
        if isinstance(expr, type(self)):
            denominators.append(expr.denominator)
            expr = expr.reduce()
        fraction = self.reduce() * expr
        return self._fraction_with_denominator(fraction, max(denominators))

    def __ne__(self, expr):
        r'''Is true when `expr` does not equal nonreduced fraction.

        ::

            >>> mathtools.NonreducedFraction(3, 3) != 'foo'
            True

        Returns boolean.
        '''
        return not self == expr

    def __neg__(self):
        r'''Negates nonreduced fraction.

        ::

            >>> -mathtools.NonreducedFraction(3, 3)
            NonreducedFraction(-3, 3)

        Returns nonreduced fraction.
        '''
        return type(self)((-self.numerator, self.denominator))

    def __pow__(self, expr):
        r'''Raises nonreduced fraction to `expr`.

        ::

            >>> mathtools.NonreducedFraction(3, 6) ** -1
            NonreducedFraction(6, 3)

        Returns nonreduced fraction.
        '''
        if expr == -1:
            return type(self)(self.denominator, self.numerator)
        return super(NonreducedFraction, self).__pow__(expr)

    def __radd__(self, expr):
        r'''Adds nonreduced fraction to `expr`.

        ::

            >>> 1 + mathtools.NonreducedFraction(3, 3)
            NonreducedFraction(6, 3)

        Returns nonreduced fraction.
        '''
        return self + expr

    def __rdiv__(self, expr):
        r'''Divides `expr` by nonreduced fraction.

        ::

            >>> 1 / mathtools.NonreducedFraction(3, 3)
            NonreducedFraction(3, 3)

        Returns nonreduced fraction.
        '''
        denominators = [self.denominator]
        if isinstance(expr, type(self)):
            denominators.append(expr.denominator)
            expr = expr.reduce()
        fraction = expr / self.reduce()
        return self._fraction_with_denominator(fraction, max(denominators))

    __rtruediv__ = __rdiv__

    def __repr__(self):
        r'''Gets interpreter representation of nonreduced fraction.

        ::

            >>> mathtools.NonreducedFraction(3, 6)
            NonreducedFraction(3, 6)

        Returns string.
        '''
        return '{}({}, {})'.format(
            type(self).__name__,
            self.numerator,
            self.denominator,
            )

    def __rmul__(self, expr):
        r'''Multiplies `expr` by nonreduced fraction.

        ::

            >>> 3 * mathtools.NonreducedFraction(3, 3)
            NonreducedFraction(9, 3)

        Returns nonreduced fraction.
        '''
        return self * expr

    def __rsub__(self, expr):
        r'''Subtracts nonreduced fraction from `expr`.

        ::

            >>> 1 - mathtools.NonreducedFraction(3, 3)
            NonreducedFraction(0, 3)

        Returns nonreduced fraction.
        '''
        return -self + expr

    def __str__(self):
        r'''String representation of nonreduced fraction.

        ::

            >>> fraction = mathtools.NonreducedFraction(-6, 3)

        ::

            >>> str(fraction)
            '-6/3'

        Returns string.
        '''
        return '{}/{}'.format(self.numerator, self.denominator)

    def __sub__(self, expr):
        r'''Subtracts `expr` from nonreduced fraction.

        ::

            >>> mathtools.NonreducedFraction(3, 3) - 2
            NonreducedFraction(-3, 3)

        Returns nonreduced fraction.
        '''
        denominators = [self.denominator]
        if isinstance(expr, type(self)):
            denominators.append(expr.denominator)
            expr = expr.reduce()
        fraction = self.reduce() - expr
        return self._fraction_with_denominator(fraction, max(denominators))

    def __truediv__(self, expr):
        r'''Divides nonreduced fraction in Python 3.

        Returns nonreduced fraction.
        '''
        return self.__div__(expr)

    ### PRIVATE PROPERTIES ###

    @property
    def _storage_format_specification(self):
        from abjad.tools import systemtools
        return systemtools.StorageFormatSpecification(
            self,
            is_indented=False,
            keyword_argument_names=(),
            positional_argument_values=(
                self.numerator,
                self.denominator,
                ),
            )

    ### PRIVATE METHODS ###

    def _fraction_with_denominator(self, fraction, denominator):
        from abjad.tools import mathtools
        denominator = mathtools.least_common_multiple(
            denominator, fraction.denominator)
        return NonreducedFraction(fraction).with_denominator(denominator)

    @staticmethod
    def _parse_input_string(string):
        if '/' in string:
            numerator, denominator = string.split('/')
            numerator = int(numerator)
            denominator = int(denominator)
        else:
            numerator = int(string)
            denominator = 1
        return numerator, denominator

    ### PUBLIC PROPERTIES ###

    @property
    def denominator(self):
        r'''Denominator of nonreduced fraction.

        ::

            >>> fraction = mathtools.NonreducedFraction(-6, 3)

        ::

            >>> fraction.denominator
            3

        Returns positive integer.
        '''
        return self._denominator

    @property
    def imag(self):
        r'''Nonreduced fractions have no imaginary part.

        ::

            >>> fraction.imag
            0

        Returns zero.
        '''
        return fractions.Fraction.imag.fget(self)

    @property
    def numerator(self):
        r'''Numerator of nonreduced fraction.

        ::

            >>> fraction = mathtools.NonreducedFraction(-6, 3)

        ::

            >>> fraction.numerator
            -6

        Returns integer.
        '''
        return self._numerator

    @property
    def pair(self):
        r'''Read only pair of nonreduced fraction numerator and denominator.

        ::

            >>> fraction = mathtools.NonreducedFraction(-6, 3)

        ::

            >>> fraction.pair
            (-6, 3)

        Returns integer pair.
        '''
        return self.numerator, self.denominator

    @property
    def real(self):
        r'''Nonreduced fractions are their own real component.

        ::

            >>> fraction.real
            NonreducedFraction(-6, 3)

        Returns nonreduced fraction.
        '''
        return self

    ### PUBLIC METHODS ###

    def multiply_with_cross_cancelation(self, multiplier):
        '''Multiplies nonreduced fraction by `expr` with cross-cancelation.

        ::

            >>> fraction = mathtools.NonreducedFraction(4, 8)

        ::

            >>> fraction.multiply_with_cross_cancelation((2, 3))
            NonreducedFraction(4, 12)

        ::

            >>> fraction.multiply_with_cross_cancelation((4, 1))
            NonreducedFraction(4, 2)

        ::

            >>> fraction.multiply_with_cross_cancelation((3, 5))
            NonreducedFraction(12, 40)

        ::

            >>> fraction.multiply_with_cross_cancelation((6, 5))
            NonreducedFraction(12, 20)

        ::

            >>> fraction = mathtools.NonreducedFraction(5, 6)
            >>> fraction.multiply_with_cross_cancelation((6, 5))
            NonreducedFraction(1, 1)

        Returns nonreduced fraction.
        '''
        from abjad.tools import durationtools
        from abjad.tools import mathtools

        multiplier = durationtools.Multiplier(multiplier)

        self_numerator_factors = mathtools.factors(self.numerator)
        multiplier_denominator_factors = mathtools.factors(
            multiplier.denominator)
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
        r'''Multiplies nonreduced fraction by `multiplier` with numerator
        preservation where possible.

        ::

            >>> fraction = mathtools.NonreducedFraction(9, 16)

        ::

            >>> fraction.multiply_with_numerator_preservation((2, 3))
            NonreducedFraction(9, 24)

        ::

            >>> fraction.multiply_with_numerator_preservation((1, 2))
            NonreducedFraction(9, 32)

        ::

            >>> fraction.multiply_with_numerator_preservation((5, 6))
            NonreducedFraction(45, 96)

        ::

            >>> fraction = mathtools.NonreducedFraction(3, 8)

        ::

            >>> fraction.multiply_with_numerator_preservation((2, 3))
            NonreducedFraction(3, 12)

        Returns nonreduced fraction.
        '''
        from abjad.tools import durationtools

        multiplier = durationtools.Multiplier(multiplier)
        self_denominator = self.denominator
        candidate_result_denominator = self_denominator / multiplier

        if candidate_result_denominator.denominator == 1:
            return NonreducedFraction(
                self.numerator, candidate_result_denominator.numerator)
        else:
            result_numerator = \
                self.numerator * candidate_result_denominator.denominator
            result_denominator = candidate_result_denominator.numerator
            return NonreducedFraction(result_numerator, result_denominator)

    def multiply_without_reducing(self, expr):
        r'''Multiplies nonreduced fraction by `expr` without reducing.

        ::

            >>> fraction = mathtools.NonreducedFraction(3, 8)

        ::

            >>> fraction.multiply_without_reducing((3, 3))
            NonreducedFraction(9, 24)

        ::

            >>> fraction = mathtools.NonreducedFraction(4, 8)

        ::

            >>> fraction.multiply_without_reducing((4, 5))
            NonreducedFraction(16, 40)

        ::

            >>> fraction.multiply_without_reducing((3, 4))
            NonreducedFraction(12, 32)

        Returns nonreduced fraction.
        '''
        expr = NonreducedFraction(expr)
        numerator = self.numerator * expr.numerator
        denominator = self.denominator * expr.denominator
        return NonreducedFraction(numerator, denominator)

    def reduce(self):
        r'''Reduces nonreduced fraction.

        ::

            >>> fraction = mathtools.NonreducedFraction(-6, 3)

        ::

            >>> fraction.reduce()
            Fraction(-2, 1)

        Returns fraction.
        '''
        return fractions.Fraction(self.numerator, self.denominator)

    def with_denominator(self, denominator):
        r'''Returns new nonreduced fraction with integer `denominator`.

        ::

            >>> mathtools.NonreducedFraction(3, 6).with_denominator(12)
            NonreducedFraction(6, 12)

        Returns nonreduced fraction.
        '''
        from abjad.tools import durationtools
        n, d = self.pair
        multiplier = durationtools.Multiplier(denominator, d)
        new_numerator = multiplier * n
        new_denominator = multiplier * d
        if new_numerator.denominator == 1 and \
            new_denominator.denominator == 1:
            return type(self)(
                new_numerator.numerator, new_denominator.numerator)
        else:
            return type(self)(n, d)

    def with_multiple_of_denominator(self, denominator):
        r'''Returns new nonreduced fraction with multiple of integer
        `denominator`.

        ::

            >>> fraction = mathtools.NonreducedFraction(3, 6)

        ::

            >>> fraction.with_multiple_of_denominator(5)
            NonreducedFraction(5, 10)

        Returns nonreduced fraction.
        '''
        result = self.with_denominator(denominator)
        while not result.denominator == denominator:
            denominator *= 2
            result = result.with_denominator(denominator)
        return result