import collections
import dataclasses
import typing

import quicktions

from . import duration as _duration
from . import math as _math


@dataclasses.dataclass(slots=True, unsafe_hash=True)
class NonreducedRatio(collections.abc.Sequence):
    """
    Nonreduced ratio.

    ..  container:: example

        Initializes from numbers:

        >>> abjad.NonreducedRatio((2, 4))
        NonreducedRatio(numbers=(2, 4))

        >>> abjad.NonreducedRatio((2, 4, 2))
        NonreducedRatio(numbers=(2, 4, 2))

        Initializes from string:

        >>> abjad.NonreducedRatio("2:4")
        NonreducedRatio(numbers=(2, 4))

        >>> abjad.NonreducedRatio("2:4:2")
        NonreducedRatio(numbers=(2, 4, 2))

    """

    numbers: typing.Sequence[int] = (1, 1)

    def __post_init__(self):
        if isinstance(self.numbers, type(self)):
            self.numbers = self.numbers.numbers
        elif isinstance(self.numbers, str):
            strings = self.numbers.split(":")
            self.numbers = [int(_) for _ in strings]
        self.numbers = tuple(self.numbers)

    def __contains__(self, argument):
        """
        Is true when ratio contains ``argument``.

        Returns true or false.
        """
        return argument in self.numbers

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
            return tuple(self.numbers.__getitem__(argument))
        return self.numbers.__getitem__(argument)

    def __iter__(self):
        """
        Iterates ratio.

        Returns generator.
        """
        return iter(self.numbers)

    def __len__(self):
        """
        Gets length of ratio.

        ..  container:: example

            >>> ratio = abjad.NonreducedRatio((2, 4, 2))
            >>> len(ratio)
            3

        Returns integer.
        """
        return len(self.numbers)

    def __reversed__(self):
        """
        Iterates ratio in reverse.

        Returns generator.
        """
        return reversed(self.numbers)

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
        multipliers = [_duration.Multiplier((_, weight)) for _ in self.numbers]
        multipliers = tuple(multipliers)
        return multipliers

    def count(self, argument):
        """
        Gets count of ``argument`` in ratio.

        Returns integer.
        """
        return self.numbers.count(argument)

    def index(self, argument):
        """
        Gets index of ``argument`` in ratio.

        Returns integer.
        """
        return self.numbers.index(argument)


@dataclasses.dataclass(slots=True, unsafe_hash=True)
class Ratio(NonreducedRatio):
    """
    Ratio.

    ..  container:: example

        Initializes from numbers:

        >>> abjad.Ratio((2, 4))
        Ratio(numbers=(1, 2))

        >>> abjad.Ratio((2, 4, 2))
        Ratio(numbers=(1, 2, 1))

    ..  container:: example

        Initializes from string:

        >>> abjad.Ratio("2:4")
        Ratio(numbers=(1, 2))

        >>> abjad.Ratio("2:4:2")
        Ratio(numbers=(1, 2, 1))

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

    def __post_init__(self):
        if isinstance(self.numbers, type(self)):
            self.numbers = self.numbers.numbers
        elif isinstance(self.numbers, str):
            strings = self.numbers.split(":")
            self.numbers = [int(_) for _ in strings]
        self.numbers = [int(_) for _ in self.numbers]
        gcd = _math.greatest_common_divisor(*self.numbers)
        self.numbers = [_ // gcd for _ in self.numbers]
        self.numbers = tuple(self.numbers)

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
            return tuple(self.numbers.__getitem__(argument))
        return self.numbers.__getitem__(argument)

    def __len__(self):
        """
        Gets length of ratio.

        ..  container:: example

            >>> ratio = abjad.Ratio((2, 4, 2))
            >>> len(ratio)
            3

        Returns integer.
        """
        return len(self.numbers)

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
        multipliers = [_duration.Multiplier((_, weight)) for _ in self.numbers]
        multipliers = tuple(multipliers)
        return multipliers

    @property
    def reciprocal(self):
        """
        Gets reciprocal.

        ..  container:: example

            Gets reciprocal:

            >>> abjad.Ratio((3, 2)).reciprocal
            Ratio(numbers=(2, 3))

            >>> abjad.Ratio((3, 2, 7)).reciprocal
            Ratio(numbers=(7, 2, 3))

        Returns new ratio.
        """
        numbers = list(reversed(self.numbers))
        return type(self)(numbers)

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
        if not _math.is_integer_equivalent_number(n):
            raise TypeError(f"is not integer-equivalent number: {n!r}.")
        ratio = self.numbers
        if not all(_math.is_integer_equivalent_number(part) for part in ratio):
            message = f"some parts in {ratio!r} not integer-equivalent numbers."
            raise TypeError(message)
        result = [0]
        divisions = [float(abs(n)) * abs(part) / _math.weight(ratio) for part in ratio]
        cumulative_divisions = _math.cumulative_sums(divisions, start=None)
        for division in cumulative_divisions:
            rounded_division = int(round(division)) - sum(result)
            if division - round(division) == 0.5:
                rounded_division += 1
            result.append(rounded_division)
        result = result[1:]
        if _math.sign(n) == -1:
            result = [-x for x in result]
        ratio_signs = [_math.sign(x) for x in ratio]
        result = [pair[0] * pair[1] for pair in zip(ratio_signs, result)]
        return result
