try:
    import quicktions as fractions # type: ignore
except ImportError:
    import fractions # type: ignore
import typing
from abjad import system
from abjad.system.AbjadObject import AbjadObject


class NonreducedFraction(AbjadObject, fractions.Fraction):
    """
    Nonreduced fraction.

    ..  container:: example

        Initializes with an integer numerator and integer denominator:

        >>> abjad.NonreducedFraction(3, 6)
        NonreducedFraction(3, 6)

    ..  container:: example

        Initializes with only an integer denominator:

        >>> abjad.NonreducedFraction(3)
        NonreducedFraction(3, 1)

    ..  container:: example

        Initializes with an integer pair:

        >>> abjad.NonreducedFraction((3, 6))
        NonreducedFraction(3, 6)

    ..  container:: example

        Initializes with an integer singleton:

        >>> abjad.NonreducedFraction((3,))
        NonreducedFraction(3, 1)

    ..  container:: example

        Nonreduced fractions inherit from built-in fraction:

        >>> isinstance(abjad.NonreducedFraction(3, 6), abjad.Fraction)
        True

    ..  container:: example

        Nonreduced fractions are numbers:

        >>> import numbers

        >>> isinstance(abjad.NonreducedFraction(3, 6), numbers.Number)
        True

    """

    ### CLASS VARIABLES ###

    __slots__ = (
        '_numerator',
        '_denominator',
        )

    ### CONSTRUCTOR ###

    def __new__(class_, *arguments):
        import abjad
        is_fraction_like = False
        if len(arguments) == 1:
            try:
                numerator = arguments[0].numerator
                denominator = arguments[0].denominator
                is_fraction_like = True
            except AttributeError:
                pass
        if is_fraction_like:
            pass
        elif len(arguments) == 1 and isinstance(arguments[0], int):
            numerator = arguments[0]
            denominator = 1
        elif (len(arguments) == 1 and
            isinstance(arguments[0], tuple) and
            len(arguments[0]) == 1):
            numerator = arguments[0][0]
            denominator = 1
        elif (len(arguments) == 1 and
            isinstance(arguments[0], tuple) and
            isinstance(arguments[0][0], int) and
            isinstance(arguments[0][1], int)):
            numerator, denominator = arguments[0]
        elif len(arguments) == 1 and isinstance(arguments[0], str):
            numerator, denominator = class_._parse_input_string(arguments[0])
        elif (isinstance(arguments, tuple) and
            len(arguments) == 2 and
            isinstance(arguments[0], int) and
            isinstance(arguments[1], int)):
            numerator = arguments[0]
            denominator = arguments[1]
        elif len(arguments) == 0:
            numerator = 0
            denominator = 1
        else:
            message = 'can not initialize {}: {!r}.'
            message = message.format(class_.__name__, arguments)
            raise ValueError(message)
        numerator *= abjad.mathtools.sign(denominator)
        denominator = abs(denominator)
        self = fractions.Fraction.__new__(class_, numerator, denominator)
        self._numerator = numerator
        self._denominator = denominator
        return self

    def __init__(self, *arguments):
        """
        Dummy initializer to satisfy mypy.
        """
        pass

    ### SPECIAL METHODS ###

    def __abs__(self):
        """
        Gets absolute value of nonreduced fraction.

        ..  container:: example

            >>> abs(abjad.NonreducedFraction(-3, 3))
            NonreducedFraction(3, 3)

        Returns nonreduced fraction.
        """
        pair = (abs(self.numerator), self.denominator)
        return self._from_pair(pair)

    def __add__(self, argument):
        """
        Adds ``argument`` to nonreduced fraction.

        ..  container:: example

            >>> abjad.NonreducedFraction(3, 3) + 1
            NonreducedFraction(6, 3)

            >>> 1 + abjad.NonreducedFraction(3, 3)
            NonreducedFraction(6, 3)

        Returns nonreduced fraction.
        """
        import abjad
        if isinstance(argument, int):
            numerator = self.numerator + argument * self.denominator
            pair = (numerator, self.denominator)
            return self._from_pair(pair)
        if getattr(argument, 'denominator', 'foo') == 'foo':
            raise ValueError(argument)
        if self.denominator == argument.denominator:
            numerator = self.numerator + argument.numerator
            pair = (numerator, self.denominator)
            return self._from_pair(pair)
        else:
            denominators = [self.denominator, argument.denominator]
            denominator = abjad.mathtools.least_common_multiple(*denominators)
            self_multiplier = denominator // self.denominator
            argument_multiplier = denominator // argument.denominator
            self_numerator = self_multiplier * self.numerator
            argument_numerator = argument_multiplier * argument.numerator
            pair = (self_numerator + argument_numerator, denominator)
            return self._from_pair(pair)

    def __div__(self, argument):
        """
        Divides nonreduced fraction by ``argument``.

        ..  container:: example

            >>> abjad.NonreducedFraction(3, 3) / 1
            NonreducedFraction(3, 3)

        Returns nonreduced fraction.
        """
        denominators = [self.denominator]
        if isinstance(argument, type(self)):
            denominators.append(argument.denominator)
            argument = argument.reduce()
        fraction = self.reduce() / argument
        return self._fraction_with_denominator(fraction, max(denominators))

    def __eq__(self, argument):
        """
        Is true when ``argument`` equals nonreduced fraction.

        ..  container:: example

            >>> abjad.NonreducedFraction(3, 3) == 1
            True

        Returns true or false.
        """
        return self.reduce() == argument

    def __format__(self, format_specification=''):
        """
        Formats nonreduced fraction.

        ..  container:: example

            >>> fraction = abjad.NonreducedFraction(-6, 3)
            >>> print(format(fraction))
            abjad.NonreducedFraction(-6, 3)

        Returns string.
        """
        if format_specification in ('', 'storage'):
            return system.StorageFormatManager(self).get_storage_format()
        return str(self)

    def __ge__(self, argument):
        """
        Is true when nonreduced fraction is greater than or equal to
        ``argument``.

        ..  container:: example

            >>> abjad.NonreducedFraction(3, 3) >= 1
            True

        Returns true or false.
        """
        return self.reduce() >= argument

    def __gt__(self, argument):
        """
        Is true when nonreduced fraction is greater than ``argument``.

        ..  container:: example

            >>> abjad.NonreducedFraction(3, 3) > 1
            False

        Returns true or false.
        """
        return self.reduce() > argument

    def __hash__(self):
        """
        Hashes nonreduced fraction.

        Required to be explicitly redefined on Python 3 if __eq__ changes.

        Returns integer.
        """
        return super().__hash__()

    def __le__(self, argument):
        """
        Is true when nonreduced fraction is less than or equal to ``argument``.

        ..  container:: example

            >>> abjad.NonreducedFraction(3, 3) <= 1
            True

        Returns true or false.
        """
        return self.reduce() <= argument

    def __lt__(self, argument):
        """
        Is true when nonreduced fraction is less than ``argument``.

        ..  container:: example

            >>> abjad.NonreducedFraction(3, 3) < 1
            False

        Returns true or false.
        """
        return self.reduce() < argument

    def __mul__(self, argument):
        """
        Multiplies nonreduced fraction by ``argument``.

        ..  container:: example

            >>> abjad.NonreducedFraction(3, 3) * 3
            NonreducedFraction(9, 3)

        Returns nonreduced fraction.
        """
        denominators = [self.denominator]
        if isinstance(argument, type(self)):
            denominators.append(argument.denominator)
            argument = argument.reduce()
        fraction = self.reduce() * argument
        return self._fraction_with_denominator(fraction, max(denominators))

    def __neg__(self):
        """
        Negates nonreduced fraction.

        ..  container:: example

            >>> -abjad.NonreducedFraction(3, 3)
            NonreducedFraction(-3, 3)

        Returns nonreduced fraction.
        """
        pair = (-self.numerator, self.denominator)
        return self._from_pair(pair)

    def __pow__(self, argument):
        """
        Raises nonreduced fraction to ``argument``.

        ..  container:: example

            >>> abjad.NonreducedFraction(3, 6) ** -1
            NonreducedFraction(6, 3)

        Returns nonreduced fraction.
        """
        if argument == -1:
            pair = (self.denominator, self.numerator)
            return self._from_pair(pair)
        return super().__pow__(argument)

    def __radd__(self, argument):
        """
        Adds nonreduced fraction to ``argument``.

        ..  container:: example

            >>> 1 + abjad.NonreducedFraction(3, 3)
            NonreducedFraction(6, 3)

        Returns nonreduced fraction.
        """
        return self + argument

    def __rdiv__(self, argument):
        """
        Divides ``argument`` by nonreduced fraction.

        ..  container:: example

            >>> 1 / abjad.NonreducedFraction(3, 3)
            NonreducedFraction(3, 3)

        Returns nonreduced fraction.
        """
        denominators = [self.denominator]
        if isinstance(argument, type(self)):
            denominators.append(argument.denominator)
            argument = argument.reduce()
        fraction = argument / self.reduce()
        return self._fraction_with_denominator(fraction, max(denominators))

    __rtruediv__ = __rdiv__

    def __repr__(self):
        """
        Gets interpreter representation of nonreduced fraction.

        ..  container:: example

            >>> abjad.NonreducedFraction(3, 6)
            NonreducedFraction(3, 6)

        Returns string.
        """
        return system.StorageFormatManager(self).get_repr_format()

    def __rmul__(self, argument):
        """
        Multiplies ``argument`` by nonreduced fraction.

        ..  container:: example

            >>> 3 * abjad.NonreducedFraction(3, 3)
            NonreducedFraction(9, 3)

        Returns nonreduced fraction.
        """
        return self * argument

    def __rsub__(self, argument):
        """
        Subtracts nonreduced fraction from ``argument``.

        ..  container:: example

            >>> 1 - abjad.NonreducedFraction(3, 3)
            NonreducedFraction(0, 3)

        Returns nonreduced fraction.
        """
        return -self + argument

    def __str__(self):
        """
        Gets string representation of nonreduced fraction.

        ..  container:: example

            >>> fraction = abjad.NonreducedFraction(-6, 3)

            >>> str(fraction)
            '-6/3'

        Returns string.
        """
        return '{}/{}'.format(self.numerator, self.denominator)

    def __sub__(self, argument):
        """
        Subtracts ``argument`` from nonreduced fraction.

        ..  container:: example

            >>> abjad.NonreducedFraction(3, 3) - 2
            NonreducedFraction(-3, 3)

            >>> abjad.NonreducedFraction(5, 4) - abjad.NonreducedFraction(18, 16)
            NonreducedFraction(2, 16)

            >>> abjad.NonreducedFraction(18, 16) - abjad.NonreducedFraction(5, 4)
            NonreducedFraction(-2, 16)

        Returns nonreduced fraction.
        """
        denominators = [self.denominator]
        if isinstance(argument, type(self)):
            denominators.append(argument.denominator)
            argument = argument.reduce()
        fraction = self.reduce() - argument
        return self._fraction_with_denominator(fraction, max(denominators))

    def __truediv__(self, argument):
        """
        Divides nonreduced fraction in Python 3.

        Returns nonreduced fraction.
        """
        return self.__div__(argument)

    ### PRIVATE METHODS ###

    def _fraction_with_denominator(self, fraction, denominator):
        import abjad
        denominators = [denominator, fraction.denominator]
        denominator = abjad.mathtools.least_common_multiple(*denominators)
        result = self._from_pair(fraction)
        result = result.with_denominator(denominator)
        return result

    def _from_pair(self, pair):
        """
        Method is designed to be subclassed.
        """
        return type(self)(pair)

    def _get_format_specification(self):
        return system.FormatSpecification(
            client=self,
            repr_is_indented=False,
            storage_format_args_values=[
                self.numerator,
                self.denominator,
                ],
            storage_format_is_indented=False,
            storage_format_kwargs_names=[],
            )

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

    ### PUBLIC METHODS ###

    def multiply(self, multiplier, preserve_numerator=False):
        """
        Multiplies nonreduced fraction by ``multiplier`` with numerator
        preservation where possible.

        ..  container:: example

            >>> fraction = abjad.NonreducedFraction(9, 16)

            >>> fraction.multiply((2, 3), preserve_numerator=True)
            NonreducedFraction(9, 24)

            >>> fraction.multiply((1, 2), preserve_numerator=True)
            NonreducedFraction(9, 32)

            >>> fraction.multiply((5, 6), preserve_numerator=True)
            NonreducedFraction(45, 96)

            >>> fraction = abjad.NonreducedFraction(3, 8)

            >>> fraction.multiply((2, 3), preserve_numerator=True)
            NonreducedFraction(3, 12)

        Returns nonreduced fraction.
        """
        import abjad
        if preserve_numerator:
            multiplier = abjad.Multiplier(multiplier)
            self_denominator = self.denominator
            candidate_result_denominator = self_denominator / multiplier
            if candidate_result_denominator.denominator == 1:
                pair = (self.numerator, candidate_result_denominator.numerator)
                return self._from_pair(pair)
            else:
                denominator = candidate_result_denominator.denominator
                result_numerator = self.numerator * denominator
                result_denominator = candidate_result_denominator.numerator
                pair = (result_numerator, result_denominator)
                return self._from_pair(pair)
        else:
            return multiplier * self

    def multiply_with_cross_cancelation(self, multiplier):
        """
        Multiplies nonreduced fraction by ``argument`` with cross-cancelation.

        ..  container:: example

            >>> fraction = abjad.NonreducedFraction(4, 8)

            >>> fraction.multiply_with_cross_cancelation((2, 3))
            NonreducedFraction(4, 12)

            >>> fraction.multiply_with_cross_cancelation((4, 1))
            NonreducedFraction(4, 2)

            >>> fraction.multiply_with_cross_cancelation((3, 5))
            NonreducedFraction(12, 40)

            >>> fraction.multiply_with_cross_cancelation((6, 5))
            NonreducedFraction(12, 20)

            >>> fraction = abjad.NonreducedFraction(5, 6)
            >>> fraction.multiply_with_cross_cancelation((6, 5))
            NonreducedFraction(1, 1)

        Returns nonreduced fraction.
        """
        import abjad
        multiplier = abjad.Multiplier(multiplier)
        self_numerator_factors = abjad.mathtools.factors(self.numerator)
        multiplier_denominator_factors = abjad.mathtools.factors(
            multiplier.denominator)
        for factor in multiplier_denominator_factors[:]:
            if factor in self_numerator_factors:
                self_numerator_factors.remove(factor)
                multiplier_denominator_factors.remove(factor)
        self_denominator_factors = abjad.mathtools.factors(self.denominator)
        multiplier_numerator_factors = abjad.mathtools.factors(
            multiplier.numerator)
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
        pair = (result_numerator, result_denominator)
        return self._from_pair(pair)

    def multiply_without_reducing(self, argument):
        """
        Multiplies nonreduced fraction by ``argument`` without reducing.

        ..  container:: example

            >>> fraction = abjad.NonreducedFraction(3, 8)

            >>> fraction.multiply_without_reducing((3, 3))
            NonreducedFraction(9, 24)

            >>> fraction = abjad.NonreducedFraction(4, 8)

            >>> fraction.multiply_without_reducing((4, 5))
            NonreducedFraction(16, 40)

            >>> fraction.multiply_without_reducing((3, 4))
            NonreducedFraction(12, 32)

        Returns nonreduced fraction.
        """
        argument = self._from_pair(argument)
        numerator = self.numerator * argument.numerator
        denominator = self.denominator * argument.denominator
        pair = (numerator, denominator)
        return self._from_pair(pair)

    def reduce(self):
        """
        Reduces nonreduced fraction.

        ..  container:: example

            >>> fraction = abjad.NonreducedFraction(-6, 3)

            >>> fraction.reduce()
            Fraction(-2, 1)

        Returns fraction.
        """
        return fractions.Fraction(self.numerator, self.denominator)

    def with_denominator(self, denominator):
        """
        Returns new nonreduced fraction with integer ``denominator``.

        ..  container:: example

            >>> abjad.NonreducedFraction(3, 6).with_denominator(12)
            NonreducedFraction(6, 12)

        ..  container:: example

            >>> for numerator in range(12):
            ...     fraction = abjad.NonreducedFraction(numerator, 6)
            ...     print(fraction, fraction.with_denominator(12))
            ...
            0/6 0/12
            1/6 2/12
            2/6 4/12
            3/6 6/12
            4/6 8/12
            5/6 10/12
            6/6 12/12
            7/6 14/12
            8/6 16/12
            9/6 18/12
            10/6 20/12
            11/6 22/12

            >>> for numerator in range(12):
            ...     fraction = abjad.NonreducedFraction(numerator, 6)
            ...     print(fraction, fraction.with_denominator(8))
            ...
            0/6 0/8
            1/6 1/6
            2/6 2/6
            3/6 4/8
            4/6 4/6
            5/6 5/6
            6/6 8/8
            7/6 7/6
            8/6 8/6
            9/6 12/8
            10/6 10/6
            11/6 11/6

            >>> for numerator in range(12):
            ...     fraction = abjad.NonreducedFraction(numerator, 6)
            ...     print(fraction, fraction.with_denominator(12))
            ...
            0/6 0/12
            1/6 2/12
            2/6 4/12
            3/6 6/12
            4/6 8/12
            5/6 10/12
            6/6 12/12
            7/6 14/12
            8/6 16/12
            9/6 18/12
            10/6 20/12
            11/6 22/12

        Returns nonreduced fraction.
        """
        import abjad
        current_numerator, current_denominator = self.pair
        multiplier = abjad.Multiplier(denominator, current_denominator)
        new_numerator = multiplier * current_numerator
        new_denominator = multiplier * current_denominator
        if (new_numerator.denominator == 1 and
            new_denominator.denominator == 1):
            pair = (new_numerator.numerator, new_denominator.numerator)
        else:
            pair = (current_numerator, current_denominator)
        return self._from_pair(pair)

    def with_multiple_of_denominator(self, denominator):
        """
        Returns new nonreduced fraction with multiple of integer
        ``denominator``.

        ..  container:: example

            >>> fraction = abjad.NonreducedFraction(3, 6)

            >>> fraction.with_multiple_of_denominator(5)
            NonreducedFraction(5, 10)

        ..  container:: example

            >>> abjad.NonreducedFraction(1, 2).with_multiple_of_denominator(2)
            NonreducedFraction(1, 2)

            >>> abjad.NonreducedFraction(1, 2).with_multiple_of_denominator(4)
            NonreducedFraction(2, 4)

            >>> abjad.NonreducedFraction(1, 2).with_multiple_of_denominator(8)
            NonreducedFraction(4, 8)

            >>> abjad.NonreducedFraction(1, 2).with_multiple_of_denominator(16)
            NonreducedFraction(8, 16)

        Returns nonreduced fraction.
        """
        result = self.with_denominator(denominator)
        while not result.denominator == denominator:
            denominator *= 2
            result = result.with_denominator(denominator)
        return result

    ### PUBLIC PROPERTIES ###

    @property
    def denominator(self):
        """
        Denominator of nonreduced fraction.

        >>> fraction = abjad.NonreducedFraction(-6, 3)

        >>> fraction.denominator
        3

        Returns positive integer.
        """
        return self._denominator

    @property
    def imag(self):
        """
        Nonreduced fractions have no imaginary part.

        >>> fraction = abjad.NonreducedFraction(-6, 3)

        >>> fraction.imag
        0

        Returns zero.
        """
        return 0

    @property
    def numerator(self):
        """
        Numerator of nonreduced fraction.

        >>> fraction = abjad.NonreducedFraction(-6, 3)

        >>> fraction.numerator
        -6

        Returns integer.
        """
        return self._numerator

    @property
    def pair(self):
        """
        Read only pair of nonreduced fraction numerator and denominator.

        >>> fraction = abjad.NonreducedFraction(-6, 3)

        >>> fraction.pair
        (-6, 3)

        Returns integer pair.
        """
        return self.numerator, self.denominator

    @property
    def real(self):
        """
        Nonreduced fractions are their own real component.

        >>> fraction = abjad.NonreducedFraction(-6, 3)

        >>> fraction.real
        NonreducedFraction(-6, 3)

        Returns nonreduced fraction.
        """
        return self
