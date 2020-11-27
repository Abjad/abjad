import collections
import typing

import quicktions

from . import math
from .duration import Multiplier
from .storage import FormatSpecification, StorageFormatManager


class NonreducedRatio(collections.abc.Sequence):
    """
    Nonreduced ratio.

    ..  container:: example

        Initializes from numbers:

        >>> abjad.NonreducedRatio((2, 4))
        NonreducedRatio((2, 4))

        >>> abjad.NonreducedRatio((2, 4, 2))
        NonreducedRatio((2, 4, 2))

    ..  container:: example

        Initializes from string:

        >>> abjad.NonreducedRatio("2:4")
        NonreducedRatio((2, 4))

        >>> abjad.NonreducedRatio("2:4:2")
        NonreducedRatio((2, 4, 2))

    """

    ### CLASS VARIABLES ###

    __slots__ = ("_numbers",)

    ### INITIALIZER ###

    def __init__(self, numbers=(1, 1)):
        if isinstance(numbers, type(self)):
            numbers = numbers.numbers
        elif isinstance(numbers, str):
            strings = numbers.split(":")
            numbers = [int(_) for _ in strings]
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
        return StorageFormatManager.compare_objects(self, argument)

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

    def __repr__(self) -> str:
        """
        Gets interpreter representation.
        """
        return StorageFormatManager(self).get_repr_format()

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

            >>> 1 / abjad.Ratio((1, 1, 3))
            [Fraction(1, 5), Fraction(1, 5), Fraction(3, 5)]

        ..  container:: example

            >>> 1.0 / abjad.Ratio((1, 1, 3))
            [0.2, 0.2, 0.6]

        Returns list of fractions or list of floats.
        """
        denominator = sum(self.numbers)
        factors = [quicktions.Fraction(_, denominator) for _ in self.numbers]
        result = [_ * number for _ in factors]
        return result

    __rdiv__ = __rtruediv__

    ### PRIVATE METHODS ###

    def _get_format_specification(self):
        return FormatSpecification(
            client=self,
            storage_format_args_values=[self.numbers],
            storage_format_is_indented=False,
            storage_format_keyword_names=[],
        )

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
        weight = sum(self.numbers)
        multipliers = [Multiplier((_, weight)) for _ in self.numbers]
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


class Ratio(NonreducedRatio):
    """
    Ratio.

    ..  container:: example

        Initializes from numbers:

        >>> abjad.Ratio((2, 4))
        Ratio((1, 2))

        >>> abjad.Ratio((2, 4, 2))
        Ratio((1, 2, 1))

    ..  container:: example

        Initializes from string:

        >>> abjad.Ratio("2:4")
        Ratio((1, 2))

        >>> abjad.Ratio("2:4:2")
        Ratio((1, 2, 1))

    """

    ### CLASS VARIABLES ###

    __slots__ = ()

    ### INITIALIZER ###

    def __init__(self, numbers=(1, 1)):
        if isinstance(numbers, type(self)):
            numbers = numbers.numbers
        elif isinstance(numbers, str):
            strings = numbers.split(":")
            numbers = [int(_) for _ in strings]
        numbers = [int(_) for _ in numbers]
        gcd = math.greatest_common_divisor(*numbers)
        numbers = [_ // gcd for _ in numbers]
        self._numbers = tuple(numbers)

    ### SPECIAL METHODS ###

    def __eq__(self, argument):
        """
        Is true when ``argument`` equals ratio.

        ..  container:: example

            >>> ratio_1 = abjad.Ratio((1, 2, 1))
            >>> ratio_2 = abjad.Ratio((1, 2, 1))
            >>> ratio_3 = abjad.Ratio((2, 3, 3))

            >>> ratio_1 == ratio_1
            True

            >>> ratio_1 == ratio_2
            True

            >>> ratio_1 == ratio_3
            False

            >>> ratio_2 == ratio_1
            True

            >>> ratio_2 == ratio_2
            True

            >>> ratio_2 == ratio_3
            False

            >>> ratio_3 == ratio_1
            False

            >>> ratio_3 == ratio_2
            False

            >>> ratio_3 == ratio_3
            True

        """
        return super().__eq__(argument)

    def __getitem__(self, argument):
        """
        Gets item or slice identified by ``argument``.

        ..  container:: example

            >>> ratio = abjad.Ratio((2, 4, 2))
            >>> ratio[1]
            2

        Returns integer or tuple.
        """
        if isinstance(argument, slice):
            return tuple(self._numbers.__getitem__(argument))
        return self._numbers.__getitem__(argument)

    def __hash__(self):
        """
        Hashes ratio.

        Required to be explicitly redefined on Python 3 if __eq__ changes.

        Returns integer.
        """
        return super().__hash__()

    def __len__(self):
        """
        Gets length of ratio.

        ..  container:: example

            >>> ratio = abjad.Ratio((2, 4, 2))
            >>> len(ratio)
            3

        Returns integer.
        """
        return len(self._numbers)

    def __str__(self):
        """
        Gets string representation of ratio.

        ..  container:: example

            Ratio of two numbers:

            >>> str(abjad.Ratio((2, 4)))
            '1:2'

        ..  container:: example

            Ratio of three numbers:

            >>> str(abjad.Ratio((2, 4, 2)))
            '1:2:1'

        Returns string.
        """
        numbers = (str(x) for x in self.numbers)
        return ":".join(numbers)

    ### PUBLIC PROPERTIES ###

    @property
    def multipliers(self):
        """
        Gets multipliers of ratio.

        ..  container:: example

            Ratio of two numbers:

            >>> ratio = abjad.Ratio((2, 4))
            >>> ratio.multipliers
            (Multiplier(1, 3), Multiplier(2, 3))

        ..  container:: example

            Ratio of three numbers:

            >>> ratio = abjad.Ratio((2, 4, 2))
            >>> ratio.multipliers
            (Multiplier(1, 4), Multiplier(1, 2), Multiplier(1, 4))

        Returns tuple of multipliers.
        """
        weight = sum(self.numbers)
        multipliers = [Multiplier((_, weight)) for _ in self.numbers]
        multipliers = tuple(multipliers)
        return multipliers

    @property
    def numbers(self):
        """
        Gets numbers of ratio.

        ..  container:: example

            Ratio of two numbers:

            >>> ratio = abjad.Ratio((2, 4))
            >>> ratio.numbers
            (1, 2)

        ..  container:: example

            Ratio of three numbers:

            >>> ratio = abjad.Ratio((2, 4, 2))
            >>> ratio.numbers
            (1, 2, 1)

        Set to tuple of two or more numbers.

        Returns tuple of two or more numbers.
        """
        return self._numbers

    @property
    def reciprocal(self):
        """
        Gets reciprocal.

        ..  container:: example

            Gets reciprocal:

            >>> abjad.Ratio((3, 2)).reciprocal
            Ratio((2, 3))

            >>> abjad.Ratio((3, 2, 7)).reciprocal
            Ratio((7, 2, 3))

        Returns new ratio.
        """
        numbers = list(reversed(self.numbers))
        return type(self)(numbers)

    ### PUBLIC METHODS ###

    def partition_integer(self, n) -> typing.List[int]:
        """
        Partitions positive integer-equivalent ``n`` by ``ratio``.

        ..  container:: example

            >>> abjad.Ratio([1, 2]).partition_integer(10)
            [3, 7]

        ..  container:: example

            Partitions positive integer-equivalent ``n`` by ``ratio`` with negative
            parts:

            >>> abjad.Ratio([1, -2]).partition_integer(10)
            [3, -7]

        ..  container:: example

            Partitions negative integer-equivalent ``n`` by ``ratio``:

            >>> abjad.Ratio([1, 2]).partition_integer(-10)
            [-3, -7]

        ..  container:: example

            Partitions negative integer-equivalent ``n`` by ``ratio`` with negative
            parts:

            >>> abjad.Ratio([1, -2]).partition_integer(-10)
            [-3, 7]

        ..  container:: example

            More examples:

            >>> abjad.Ratio([1]).partition_integer(10)
            [10]

            >>> abjad.Ratio([1, 1]).partition_integer(10)
            [5, 5]

            >>> abjad.Ratio([1, -1, -1]).partition_integer(10)
            [3, -4, -3]

            >>> abjad.Ratio([1, 1, 1, 1]).partition_integer(-10)
            [-3, -2, -3, -2]

            >>> abjad.Ratio([1, 1, 1, 1, 1]).partition_integer(-10)
            [-2, -2, -2, -2, -2]

        Returns result with weight equal to absolute value of ``n``.
        """
        if not math.is_integer_equivalent_number(n):
            raise TypeError(f"is not integer-equivalent number: {n!r}.")
        ratio = self.numbers
        if not all(math.is_integer_equivalent_number(part) for part in ratio):
            message = f"some parts in {ratio!r} not integer-equivalent numbers."
            raise TypeError(message)
        result = [0]
        divisions = [float(abs(n)) * abs(part) / math.weight(ratio) for part in ratio]
        cumulative_divisions = math.cumulative_sums(divisions, start=None)
        for division in cumulative_divisions:
            rounded_division = int(round(division)) - sum(result)
            if division - round(division) == 0.5:
                rounded_division += 1
            result.append(rounded_division)
        result = result[1:]
        if math.sign(n) == -1:
            result = [-x for x in result]
        ratio_signs = [math.sign(x) for x in ratio]
        result = [pair[0] * pair[1] for pair in zip(ratio_signs, result)]
        return result
