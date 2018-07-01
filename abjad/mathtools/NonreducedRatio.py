import collections
import fractions
from abjad.system.AbjadValueObject import AbjadValueObject


class NonreducedRatio(AbjadValueObject, collections.Sequence):
    """
    Nonreduced ratio.

    ..  container:: example

        Nonreduced ratio of two numbers:

        >>> abjad.NonreducedRatio((2, 4))
        NonreducedRatio((2, 4))

    ..  container:: example

        Nonreduced ratio of three numbers:

            >>> abjad.NonreducedRatio((2, 4, 2))
            NonreducedRatio((2, 4, 2))

    """

    ### CLASS VARIABLES ###

    __slots__ = (
        '_numbers',
        )

    ### INITIALIZER ###

    def __init__(self, numbers=(1, 1)):
        if isinstance(numbers, type(self)):
            numbers = numbers.numbers
        numbers = tuple(numbers)
        self._numbers = numbers

    ### SPECIAL METHODS ###

    def __contains__(self, argument):
        """
        Is true when ratio contains ``argument``.

        Returns true or false.
        """
        return argument in self._numbers

    def __eq__(self, argument):
        """
        Is true when ``argument`` is a nonreduced ratio with numerator and
        denominator equal to those of this nonreduced ratio.

        Returns true or false.
        """
        return super().__eq__(argument)

    def __format__(self, format_specification=''):
        """
        Formats duration.

        ..  container:: example

            >>> ratio = abjad.NonreducedRatio((2, 4, 2))
            >>> print(format(ratio))
            abjad.NonreducedRatio((2, 4, 2))

        Returns string.
        """
        import abjad
        if format_specification in ('', 'storage'):
            return abjad.StorageFormatManager(self).get_storage_format()
        return str(self)

    def __getitem__(self, argument):
        """
        Gets item or slice identified by ``argument``.

        ..  container:: example

            >>> ratio = abjad.NonreducedRatio((2, 4, 2))
            >>> ratio[1]
            4

        Returns integer or tuple.
        """
        if isinstance(argument, slice):
            return tuple(self._numbers.__getitem__(argument))
        return self._numbers.__getitem__(argument)

    def __hash__(self):
        """
        Hashes non-reduced ratio.

        Required to be explicitly redefined on Python 3 if __eq__ changes.

        Returns integer.
        """
        return super().__hash__()

    def __iter__(self):
        """
        Iterates ratio.

        Returns generator.
        """
        return iter(self._numbers)

    def __len__(self):
        """
        Gets length of ratio.

        ..  container:: example

            >>> ratio = abjad.NonreducedRatio((2, 4, 2))
            >>> len(ratio)
            3

        Returns integer.
        """
        return len(self._numbers)

    def __reversed__(self):
        """
        Iterates ratio in reverse.

        Returns generator.
        """
        return reversed(self._numbers)

    def __rtruediv__(self, number):
        """
        Divides ``number`` by ratio.

        ..  container:: example

            >>> 1 / abjad.Ratio((1, 1, 3))
            [Fraction(1, 5), Fraction(1, 5), Fraction(3, 5)]

        ..  container:: example

            >>> abjad.Fraction(1) / abjad.Ratio((1, 1, 3))
            [Fraction(1, 5), Fraction(1, 5), Fraction(3, 5)]

        ..  container:: example

            >>> 1.0 / abjad.Ratio((1, 1, 3))
            [0.2, 0.2, 0.6]

        Returns list of fractions or list of floats.
        """
        denominator = sum(self.numbers)
        factors = [fractions.Fraction(_, denominator) for _ in self.numbers]
        result = [_ * number for _ in factors]
        return result

    __rdiv__ = __rtruediv__

    ### PRIVATE METHODS ###

    def _get_format_specification(self):
        import abjad
        return abjad.FormatSpecification(
            client=self,
            storage_format_args_values=[self.numbers],
            storage_format_is_indented=False,
            storage_format_kwargs_names=[],
            )

    ### PRIVATE PROPERTIES ###

    @property
    def _number_coercer(self):
        return int

    ### PUBLIC PROPERTIES ###

    @property
    def multipliers(self):
        """
        Gets multipliers of nonreduced ratio.

        ..  container:: example

            Nonreduced ratio of two numbers:

            >>> ratio = abjad.NonreducedRatio((2, 4))
            >>> ratio.multipliers
            (Multiplier(1, 3), Multiplier(2, 3))

        ..  container:: example

            Nonreduced ratio of three numbers:

            >>> ratio = abjad.NonreducedRatio((2, 4, 2))
            >>> ratio.multipliers
            (Multiplier(1, 4), Multiplier(1, 2), Multiplier(1, 4))

        Returns tuple of multipliers.
        """
        import abjad
        weight = sum(self.numbers)
        multipliers = [
            abjad.Multiplier((_, weight))
            for _ in self.numbers
            ]
        multipliers = tuple(multipliers)
        return multipliers

    @property
    def numbers(self):
        """
        Gets numbers of nonreduced ratio.

        ..  container:: example

            Nonreduced ratio of two numbers:

            >>> ratio = abjad.NonreducedRatio((2, 4))
            >>> ratio.numbers
            (2, 4)

        ..  container:: example

            Nonreduced ratio of three numbers:

            >>> ratio = abjad.NonreducedRatio((2, 4, 2))
            >>> ratio.numbers
            (2, 4, 2)

        Set to tuple of two or more numbers.

        Returns tuple of two or more numbers.
        """
        return self._numbers

    ### PUBLIC METHODS ###

    def count(self, argument):
        """
        Gets count of ``argument`` in ratio.

        Returns integer.
        """
        return self._numbers.count(argument)

    def index(self, argument):
        """
        Gets index of ``argument`` in ratio.

        Returns integer.
        """
        return self._numbers.index(argument)
