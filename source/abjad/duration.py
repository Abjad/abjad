"""
Duration, offset, ratio.
"""

from __future__ import annotations

import dataclasses
import fractions
import functools
import math
import re
import typing

from . import exceptions as _exceptions
from . import math as _math


def is_fraction(argument: object) -> bool:
    """
    Is true when ``argument`` is fraction (but not duration).

    ..  container:: example

        >>> abjad.duration.is_fraction(abjad.Fraction(1, 4))
        True

        >>> abjad.duration.is_fraction(abjad.Offset(abjad.Fraction(1, 4)))
        False

        >>> abjad.duration.is_fraction((1, 4))
        False

        >>> abjad.duration.is_fraction(0)
        False

    """
    return type(argument).__name__ == "Fraction"


def is_offset(argument: object) -> bool:
    """
    Is true when ``argument`` is offset.

    ..  container:: example

        >>> abjad.duration.is_offset(abjad.Fraction(1, 4))
        False

        >>> abjad.duration.is_offset(abjad.Offset(abjad.Fraction(1, 4)))
        True

        >>> abjad.duration.is_offset((1, 4))
        False

        >>> abjad.duration.is_offset(0)
        False

    """
    return type(argument).__name__ == "Offset"


def offset(n: int, d: int | None = None) -> Offset:
    """
    Makes offset from ``n``.

    ..  container:: example

        >>> abjad.duration.offset(1)
        Offset(Fraction(1, 1))

    """
    assert isinstance(n, int), repr(n)
    if d is not None:
        assert isinstance(d, int), repr(d)
    fraction = fractions.Fraction(n, d)
    return Offset(fraction)


def pair_with_denominator(
    fraction: fractions.Fraction, denominator: int
) -> tuple[int, int]:
    """
    Spells ``fraction`` as pair with ``denominator``.

    ..  container:: example

        >>> for numerator in range(12):
        ...     fraction = abjad.Fraction(numerator, 6)
        ...     pair = abjad.duration.pair_with_denominator(fraction, 6)
        ...     print(fraction, pair)
        ...
        0       (0, 6)
        1/6     (1, 6)
        1/3     (2, 6)
        1/2     (3, 6)
        2/3     (4, 6)
        5/6     (5, 6)
        1       (6, 6)
        7/6     (7, 6)
        4/3     (8, 6)
        3/2     (9, 6)
        5/3     (10, 6)
        11/6    (11, 6)

        >>> for numerator in range(12):
        ...     fraction = abjad.Fraction(numerator, 6)
        ...     pair = abjad.duration.pair_with_denominator(fraction, 8)
        ...     print(fraction, pair)
        ...
        0       (0, 8)
        1/6     (1, 6)
        1/3     (1, 3)
        1/2     (4, 8)
        2/3     (2, 3)
        5/6     (5, 6)
        1       (8, 8)
        7/6     (7, 6)
        4/3     (4, 3)
        3/2     (12, 8)
        5/3     (5, 3)
        11/6    (11, 6)

        >>> for numerator in range(12):
        ...     fraction = abjad.Fraction(numerator, 6)
        ...     pair = abjad.duration.pair_with_denominator(fraction, 12)
        ...     print(fraction, pair)
        ...
        0       (0, 12)
        1/6     (2, 12)
        1/3     (4, 12)
        1/2     (6, 12)
        2/3     (8, 12)
        5/6     (10, 12)
        1       (12, 12)
        7/6     (14, 12)
        4/3     (16, 12)
        3/2     (18, 12)
        5/3     (20, 12)
        11/6    (22, 12)

    """
    assert isinstance(fraction, fractions.Fraction), repr(fraction)
    current_numerator = fraction.numerator
    current_denominator = fraction.denominator
    multiplier = fractions.Fraction(denominator, current_denominator)
    new_numerator = multiplier * current_numerator
    new_denominator = multiplier * current_denominator
    if new_numerator.denominator == 1 and new_denominator.denominator == 1:
        pair = (new_numerator.numerator, new_denominator.numerator)
    else:
        pair = (current_numerator, current_denominator)
    return pair


def value_durations(items: list) -> list[ValueDuration]:
    """
    Changes ``items`` to value durations.

    ..  container:: example

        >>> items = [(15, 8), (3, 8), abjad.TimeSignature((3, 4))]
        >>> abjad.duration.value_durations(items)
        [ValueDuration(numerator=15, denominator=8), ValueDuration(numerator=3, denominator=8), ValueDuration(numerator=3, denominator=4)]

    """
    durations = []
    for item in items:
        if isinstance(item, tuple):
            duration = ValueDuration(*item)
        elif callable(getattr(item, "duration", None)):
            duration = item.duration()
            assert isinstance(duration, ValueDuration), repr(duration)
        elif callable(getattr(item, "as_integer_ratio", None)):
            duration = ValueDuration(*item.as_integer_ratio())
        else:
            duration = ValueDuration(item)
        durations.append(duration)
    return durations


@functools.total_ordering
@dataclasses.dataclass(frozen=True, slots=True, unsafe_hash=True)
class ValueDuration:
    """
    Value duration.

    ..  container:: example

        >>> abjad.ValueDuration(2, 8)
        ValueDuration(numerator=1, denominator=4)

    """

    numerator: int
    denominator: int = 1

    def __post_init__(self) -> None:
        assert self.denominator != 0, repr(self.denominator)
        numerator, denominator = self.numerator, self.denominator
        if denominator < 0:
            numerator, denominator = -numerator, -denominator
        if numerator == 0:
            numerator, denominator = 0, 1
        else:
            g = math.gcd(numerator, denominator)
            numerator //= g
            denominator //= g
        object.__setattr__(self, "numerator", numerator)
        object.__setattr__(self, "denominator", denominator)

    def __abs__(self) -> ValueDuration:
        numerator, denominator = abs(self.numerator), self.denominator
        return ValueDuration(numerator, denominator)

    def __add__(self, other: int | ValueDuration) -> ValueDuration:
        if isinstance(other, int):
            other = ValueDuration(other)
        if isinstance(other, ValueDuration):
            a, b = self.numerator, self.denominator
            c, d = other.numerator, other.denominator
            return ValueDuration(a * d + c * b, b * d)
        return NotImplemented

    def __eq__(self, other: object) -> bool:
        if isinstance(other, ValueDuration):
            return self.as_integer_ratio() == other.as_integer_ratio()
        return NotImplemented

    def __float__(self) -> float:
        return float(fractions.Fraction(self.numerator, self.denominator))

    def __lt__(self, other: object) -> bool:
        if not isinstance(other, ValueDuration):
            return NotImplemented
        return self.numerator * other.denominator < other.numerator * self.denominator

    def __neg__(self) -> ValueDuration:
        numerator, denominator = self.numerator, self.denominator
        return ValueDuration(-numerator, denominator)

    def __radd__(self, other: int | ValueDuration) -> ValueDuration:
        return self.__add__(other)

    def __rmul__(self, other: int | fractions.Fraction) -> ValueDuration:
        if isinstance(other, int):
            other = fractions.Fraction(other, 1)
        if isinstance(other, fractions.Fraction):
            a, b = self.numerator, self.denominator
            c, d = other.numerator, other.denominator
            return ValueDuration(a * c, b * d)
        return NotImplemented

    def __sub__(self, other: ValueDuration) -> ValueDuration:
        if isinstance(other, ValueDuration):
            a, b = self.numerator, self.denominator
            c, d = other.numerator, other.denominator
            return ValueDuration(a * d - c * b, b * d)
        return NotImplemented

    @typing.overload
    def __truediv__(self, other: ValueDuration) -> fractions.Fraction:
        pass

    @typing.overload
    def __truediv__(self, other: int | fractions.Fraction) -> ValueDuration:
        pass

    def __truediv__(self, other):
        if isinstance(other, int):
            other = fractions.Fraction(other, 1)
        if isinstance(other, ValueDuration):
            a, b = self.numerator, self.denominator
            c, d = other.numerator, other.denominator
            return fractions.Fraction(a * d, b * c)
        if isinstance(other, fractions.Fraction):
            a, b = self.numerator, self.denominator
            c, d = other.numerator, other.denominator
            return ValueDuration(a * d, b * c)
        return NotImplemented

    def as_fraction(self) -> fractions.Fraction:
        """
        Returns value duration as fraction.

        ..  container:: example

            >>> abjad.ValueDuration(1, 4).as_fraction()
            Fraction(1, 4)

        """
        return fractions.Fraction(*self.as_integer_ratio())

    def as_integer_ratio(self) -> tuple[int, int]:
        """
        Changes duration to (numerator, denominator) pair.

        ..  container:: example

            >>> abjad.ValueDuration(1, 4).as_integer_ratio()
            (1, 4)

        """
        return self.numerator, self.denominator

    def dot_count(self) -> int:
        r"""
        Gets dot count.

        ..  container:: example

            Dot count defined equal to number of dots required to notate
            duration. Raises assignability error when duration is not
            assignable.

            >>> for n in range(1, 16 + 1):
            ...     duration = abjad.ValueDuration(n, 16)
            ...     fraction = duration.as_fraction()
            ...     sixteenths = abjad.duration.pair_with_denominator(fraction, 16)
            ...     numerator, denominator = sixteenths
            ...     try:
            ...         dot_count = duration.dot_count()
            ...         string = f"{numerator}/{denominator}\t{dot_count}"
            ...         print(string)
            ...     except abjad.AssignabilityError:
            ...         print(f"{numerator}/{denominator}\t--")
            ...
            1/16    0
            2/16    0
            3/16    1
            4/16    0
            5/16    --
            6/16    1
            7/16    2
            8/16    0
            9/16    --
            10/16   --
            11/16   --
            12/16   1
            13/16   --
            14/16   2
            15/16   3
            16/16   0

        """
        if not self.is_assignable():
            raise _exceptions.AssignabilityError
        binary_string = _math.integer_to_binary_string(self.numerator)
        digit_sum = sum([int(x) for x in list(binary_string)])
        dot_count = digit_sum - 1
        return dot_count

    def exponent(self) -> int:
        r"""
        Gets base-2 exponent.

        ..  container:: example

            >>> for numerator in range(1, 16 + 1):
            ...     duration = abjad.ValueDuration(numerator, 16)
            ...     fraction = duration.as_fraction()
            ...     exponent = duration.exponent()
            ...     sixteenths = abjad.duration.pair_with_denominator(fraction, 16)
            ...     numerator, denominator = sixteenths
            ...     print(f"{numerator}/{denominator}\t{exponent!s}")
            ...
            1/16	4
            2/16	3
            3/16	3
            4/16	2
            5/16	2
            6/16	2
            7/16	2
            8/16	1
            9/16	1
            10/16	1
            11/16	1
            12/16	1
            13/16	1
            14/16	1
            15/16	1
            16/16	0

        """
        return -int(math.floor(math.log(self, 2)))

    def flag_count(self) -> int:
        r"""
        Gets flag count.

        ..  container:: example

            Flag count defined equal to number of flags required to notate
            duration.

            >>> for n in range(1, 16 + 1):
            ...     duration = abjad.ValueDuration(n, 64)
            ...     fraction = duration.as_fraction()
            ...     sixty_fourths = abjad.duration.pair_with_denominator(fraction, 64)
            ...     numerator, denominator = sixty_fourths
            ...     flag_count = duration.flag_count()
            ...     print(f"{numerator}/{denominator}\t{flag_count}")
            ...
            1/64    4
            2/64    3
            3/64    3
            4/64    2
            5/64    2
            6/64    2
            7/64    2
            8/64    1
            9/64    1
            10/64   1
            11/64   1
            12/64   1
            13/64   1
            14/64   1
            15/64   1
            16/64   0

        """
        log = math.log(float(self.numerator) / self.denominator, 2)
        count = -int(math.floor(log)) - 2
        return max(count, 0)

    @staticmethod
    def from_clock_string(clock_string) -> ValueDuration:
        """
        Initializes duration (in seconds) from ``clock_string``.

        ..  container:: example

            >>> abjad.ValueDuration.from_clock_string("0'00''")
            ValueDuration(numerator=0, denominator=1)

            >>> abjad.ValueDuration.from_clock_string("0'59''")
            ValueDuration(numerator=59, denominator=1)

            >>> abjad.ValueDuration.from_clock_string("1'00''")
            ValueDuration(numerator=60, denominator=1)

            >>> abjad.ValueDuration.from_clock_string("1'17''")
            ValueDuration(numerator=77, denominator=1)

        """
        minutes = 0
        if "'" in clock_string:
            tick_index = clock_string.find("'")
            minutes = clock_string[:tick_index]
            minutes = int(minutes)
        seconds = clock_string[-4:-2]
        seconds = int(seconds)
        seconds = 60 * minutes + seconds
        return ValueDuration(seconds)

    @staticmethod
    def from_dot_count(dot_count: int) -> ValueDuration:
        """
        Initializes duration from ``dot_count``.

        ..  container::

            >>> abjad.ValueDuration.from_dot_count(2)
            ValueDuration(numerator=7, denominator=4)

        """
        assert isinstance(dot_count, int), repr(dot_count)
        assert 0 <= dot_count, repr(dot_count)
        denominator = 2**dot_count
        numerator = 2 ** (dot_count + 1) - 1
        duration = ValueDuration(numerator, denominator)
        return duration

    @staticmethod
    def from_lilypond_duration_string(lilypond_duration_string: str) -> ValueDuration:
        """
        Initializes duration from LilyPond duration string.

        ..  container:: example

            >>> abjad.ValueDuration.from_lilypond_duration_string("8.")
            ValueDuration(numerator=3, denominator=16)

        """
        assert isinstance(lilypond_duration_string, str), repr(lilypond_duration_string)
        numeric_body_strings = [str(2**n) for n in range(8)]
        other_body_strings = [r"\\breve", r"\\longa", r"\\maxima"]
        body_strings = numeric_body_strings + other_body_strings
        body_string = "|".join(body_strings)
        pattern = r"^(%s)(\.*)$" % body_string
        match = re.match(pattern, lilypond_duration_string)
        if match is None:
            message = f"incorrect duration string format: {lilypond_duration_string!r}."
            raise TypeError(message)
        body_string, dots_string = match.groups()
        try:
            body_denominator = int(body_string)
            body_duration = fractions.Fraction(1, body_denominator)
        except ValueError:
            if body_string == r"\breve":
                body_duration = fractions.Fraction(2)
            elif body_string == r"\longa":
                body_duration = fractions.Fraction(4)
            elif body_string == r"\maxima":
                body_duration = fractions.Fraction(8)
            else:
                raise ValueError(f"unknown body string: {body_string!r}.")
        rational = body_duration
        for n in range(len(dots_string)):
            exponent = n + 1
            denominator = 2**exponent
            multiplier = fractions.Fraction(1, denominator)
            addend = multiplier * body_duration
            rational += addend
        return ValueDuration(*rational.as_integer_ratio())

    def is_assignable(self) -> bool:
        r"""
        Is true when duration is assignable.

        ..  container:: example

            >>> for numerator in range(0, 16 + 1):
            ...     duration = abjad.ValueDuration(numerator, 16)
            ...     fraction = duration.as_fraction()
            ...     sixteenths = abjad.duration.pair_with_denominator(fraction, 16)
            ...     print(f"{sixteenths[0]}/{sixteenths[1]}\t{duration.is_assignable()}")
            ...
            0/16    False
            1/16    True
            2/16    True
            3/16    True
            4/16    True
            5/16    False
            6/16    True
            7/16    True
            8/16    True
            9/16    False
            10/16   False
            11/16   False
            12/16   True
            13/16   False
            14/16   True
            15/16   True
            16/16   True

        """
        if ValueDuration(0) < self < ValueDuration(16):
            if _math.is_nonnegative_integer_power_of_two(self.denominator):
                if _math.is_assignable_integer(self.numerator):
                    return True
        return False

    def is_dyadic(self) -> bool:
        r"""
        Is true when denominator of duration is integer power of two.

        ..  container:: example

            >>> for n in range(1, 16 + 1):
            ...     duration = abjad.ValueDuration(1, n)
            ...     result = duration.is_dyadic()
            ...     print(f"1/{n}\t{result}")
            ...
            1/1     True
            1/2     True
            1/3     False
            1/4     True
            1/5     False
            1/6     False
            1/7     False
            1/8     True
            1/9     False
            1/10    False
            1/11    False
            1/12    False
            1/13    False
            1/14    False
            1/15    False
            1/16    True

        """
        return _math.is_nonnegative_integer_power_of_two(self.denominator)

    def lilypond_duration_string(self) -> str:
        """
        Gets LilyPond duration string.

        ..  container:: example

            >>> abjad.ValueDuration(3, 16).lilypond_duration_string()
            '8.'

        """
        if not self.is_assignable():
            raise _exceptions.AssignabilityError(self)
        undotted_rational = fractions.Fraction(1, 2) ** self.exponent()
        if undotted_rational <= 1:
            undotted_duration_string = str(undotted_rational.denominator)
        elif undotted_rational == fractions.Fraction(2, 1):
            undotted_duration_string = r"\breve"
        elif undotted_rational == fractions.Fraction(4, 1):
            undotted_duration_string = r"\longa"
        elif undotted_rational == fractions.Fraction(8, 1):
            undotted_duration_string = r"\maxima"
        else:
            message = f"can not process undotted rational: {undotted_rational!r}"
            raise ValueError(message)
        dot_count = self.dot_count()
        dot_string = "." * dot_count
        dotted_duration_string = undotted_duration_string + dot_string
        return dotted_duration_string

    def pair(self) -> tuple[int, int]:
        """
        Gets (numerator, denominator) pair.
        """
        return self.numerator, self.denominator

    def reciprocal(self) -> ValueDuration:
        """
        Gets reciprocal.

        ..  container:: example

            >>> abjad.ValueDuration(3, 7).reciprocal()
            ValueDuration(numerator=7, denominator=3)

        """
        return ValueDuration(self.denominator, self.numerator)


@dataclasses.dataclass(frozen=True, order=True, slots=True, unsafe_hash=True)
class Ratio:
    """
    Ratio.

    ..  container:: example

        >>> abjad.Ratio(6, 4)
        Ratio(numerator=6, denominator=4)

    Abjad ratios are two-term, unreduced integer ratios of the form ``n:d``.

    These are used primarily in modeling tuplet ratios like ``3:2`` and ``6:4``.
    """

    numerator: int
    denominator: int

    def __post_init__(self):
        assert isinstance(self.numerator, int), repr(self.numerator)
        assert isinstance(self.denominator, int), repr(self.denominator)

    def __mul__(self, n: int) -> Ratio:
        """
        Multiplies numerator and denominator of ratio by ``n``.

        ..  container:: example

            >>> abjad.Ratio(3, 2) * 2
            Ratio(numerator=6, denominator=4)

        """
        assert isinstance(n, int), repr(n)
        return Ratio(n * self.numerator, n * self.denominator)

    def __truediv__(self, n: int) -> Ratio:
        """
        Divides numerator and denominator of ratio by ``n``.

        ..  container:: example

            >>> abjad.Ratio(6, 4) / 2
            Ratio(numerator=3, denominator=2)

        """
        assert isinstance(n, int), repr(n)
        assert self.numerator % n == 0, repr((self.numerator, n))
        assert self.denominator % n == 0, repr((self.denominator, n))
        return Ratio(self.numerator // n, self.denominator // n)

    def __rmul__(self, n: int) -> Ratio:
        """
        Multiplies numerator and denominator of ratio by ``n``.

        ..  container:: example

            >>> 2 * abjad.Ratio(3, 2)
            Ratio(numerator=6, denominator=4)

        """
        assert isinstance(n, int), repr(n)
        return Ratio(n * self.numerator, n * self.denominator)

    def __str__(self) -> str:
        """
        Gets colon-delimited string format of ratio.

        ..  container:: example

            >>> str(abjad.Ratio(6, 4))
            '6:4'

        """
        return f"{self.numerator}:{self.denominator}"

    def fraction(self):
        """
        Changes (unreduced) ratio to (reduced) fraction.

        ..  container:: example

            >>> abjad.Ratio(6, 4).fraction()
            Fraction(3, 2)

        """
        return fractions.Fraction(self.numerator, self.denominator)

    def is_augmented(self) -> bool:
        """
        Is true when ratio numerator is less than ratio denominator.

        ..  container:: example

            >>> abjad.Ratio(6, 4).is_augmented()
            False

            >>> abjad.Ratio(3, 2).is_augmented()
            False

            >>> abjad.Ratio(4, 6).is_augmented()
            True

            >>> abjad.Ratio(2, 3).is_augmented()
            True

            >>> abjad.Ratio(2, 2).is_augmented()
            False

            >>> abjad.Ratio(1, 1).is_augmented()
            False

        """
        return self.numerator < self.denominator

    def is_canonical(self) -> bool:
        """
        Is true when ratio is normalized diminution.

        ..  container:: example

            >>> abjad.Ratio(6, 4).is_canonical()
            True

            >>> abjad.Ratio(3, 2).is_canonical()
            True

            >>> abjad.Ratio(4, 6).is_canonical()
            False

            >>> abjad.Ratio(2, 3).is_canonical()
            False

            >>> abjad.Ratio(2, 2).is_canonical()
            False

            >>> abjad.Ratio(1, 1).is_canonical()
            False

        """
        return self.is_normalized() and self.is_diminished()

    def is_diminished(self) -> bool:
        """
        Is true when ratio denominator is less than ratio numerator.

        ..  container:: example

            >>> abjad.Ratio(6, 4).is_diminished()
            True

            >>> abjad.Ratio(3, 2).is_diminished()
            True

            >>> abjad.Ratio(4, 6).is_diminished()
            False

            >>> abjad.Ratio(2, 3).is_diminished()
            False

            >>> abjad.Ratio(2, 2).is_diminished()
            False

            >>> abjad.Ratio(1, 1).is_diminished()
            False

        """
        return self.denominator < self.numerator

    def is_dyadic(self) -> bool:
        """
        Is true when ratio denominator is nonnegative integer power of two.

        ..  container:: example

            >>> abjad.Ratio(6, 4).is_dyadic()
            True

            >>> abjad.Ratio(3, 2).is_dyadic()
            True

            >>> abjad.Ratio(4, 6).is_dyadic()
            False

            >>> abjad.Ratio(2, 3).is_dyadic()
            False

            >>> abjad.Ratio(2, 2).is_dyadic()
            True

            >>> abjad.Ratio(1, 1).is_dyadic()
            True

        """
        return _math.is_nonnegative_integer_power_of_two(self.denominator)

    def is_normalized(self) -> bool:
        """
        Is true when fraction form of ratio is greater than ``1/2`` and less
        than ``2``.

        ..  container:: example

            >>> abjad.Ratio(6, 4).is_normalized()
            True

            >>> abjad.Ratio(3, 2).is_normalized()
            True

            >>> abjad.Ratio(4, 6).is_normalized()
            True

            >>> abjad.Ratio(2, 3).is_normalized()
            True

            >>> abjad.Ratio(2, 2).is_normalized()
            True

            >>> abjad.Ratio(1, 1).is_normalized()
            True

        ..  container:: example

            >>> abjad.Ratio(10, 4).is_normalized()
            False

            >>> abjad.Ratio(4, 10).is_normalized()
            False

            >>> abjad.Ratio(9, 4).is_normalized()
            False

            >>> abjad.Ratio(4, 9).is_normalized()
            False

        """
        self_fraction = fractions.Fraction(self.numerator, self.denominator)
        return fractions.Fraction(1, 2) < self_fraction < fractions.Fraction(2)

    def is_reduced(self) -> bool:
        """
        Is true when ratio numerator and denominator are relatively prime.

        ..  container:: example

            >>> abjad.Ratio(6, 4).is_reduced()
            False

            >>> abjad.Ratio(3, 2).is_reduced()
            True

            >>> abjad.Ratio(4, 6).is_reduced()
            False

            >>> abjad.Ratio(2, 3).is_reduced()
            True

            >>> abjad.Ratio(2, 2).is_reduced()
            False

            >>> abjad.Ratio(1, 1).is_reduced()
            True

        """
        fraction = self.fraction()
        if self.numerator == fraction.numerator:
            if self.denominator == fraction.denominator:
                return True
        return False

    def is_trivial(self) -> bool:
        """
        Is true when ratio numerator equals ratio denominator.

        ..  container:: example

            >>> abjad.Ratio(6, 4).is_trivial()
            False

            >>> abjad.Ratio(3, 2).is_trivial()
            False

            >>> abjad.Ratio(4, 6).is_trivial()
            False

            >>> abjad.Ratio(2, 3).is_trivial()
            False

            >>> abjad.Ratio(2, 2).is_trivial()
            True

            >>> abjad.Ratio(1, 1).is_trivial()
            True

        """
        return self.numerator == self.denominator

    def reciprocal(self) -> Ratio:
        """
        Get reciprocal of ratio.

        ..  container:: example

            >>> abjad.Ratio(6, 4).reciprocal()
            Ratio(numerator=4, denominator=6)

        """
        return Ratio(self.denominator, self.numerator)


@dataclasses.dataclass(frozen=True, slots=True, unsafe_hash=True)
class Offset:
    """
    Offset.

    ..  container:: example

        >>> fraction = abjad.Fraction(3, 16)
        >>> abjad.Offset(fraction)
        Offset(Fraction(3, 16))

        >>> displacement = abjad.ValueDuration(-1, 16)
        >>> abjad.Offset(fraction, displacement=displacement)
        Offset(Fraction(3, 16), displacement=ValueDuration(numerator=-1, denominator=16))

    """

    fraction: fractions.Fraction
    displacement: ValueDuration | None = None

    def __post_init__(self):
        assert type(self.fraction).__name__ == "Fraction", repr(self.fraction)
        if self.displacement is not None:
            assert isinstance(self.displacement, ValueDuration), repr(self.displacement)

    def __add__(self, argument: int | fractions.Fraction | ValueDuration) -> Offset:
        assert isinstance(argument, int | fractions.Fraction | ValueDuration), repr(
            argument
        )
        if isinstance(argument, ValueDuration):
            fraction = argument.as_fraction()
        else:
            fraction = fractions.Fraction(argument)
        offset = Offset(self.fraction + fraction, displacement=self.displacement)
        return offset

    def __radd__(self, argument: int | fractions.Fraction | ValueDuration) -> Offset:
        assert isinstance(argument, int | fractions.Fraction | ValueDuration), repr(
            argument
        )
        if isinstance(argument, ValueDuration):
            fraction = argument.as_fraction()
        else:
            fraction = fractions.Fraction(argument)
        offset = Offset(fraction + self.fraction, displacement=self.displacement)
        return offset

    def __eq__(self, argument: object) -> bool:
        if isinstance(argument, Offset):
            if self.fraction == argument.fraction:
                if self._nonnone_displacement() == argument._nonnone_displacement():
                    return True
        return False

    def __ge__(self, argument: object) -> bool:
        if not isinstance(argument, Offset):
            raise TypeError
        if self.fraction == argument.fraction:
            return self._nonnone_displacement() >= argument._nonnone_displacement()
        return self.fraction >= argument.fraction

    def __gt__(self, argument: object) -> bool:
        if not isinstance(argument, Offset):
            raise TypeError
        if self.fraction == argument.fraction:
            return self._nonnone_displacement() > argument._nonnone_displacement()
        return self.fraction > argument.fraction

    def __le__(self, argument: object) -> bool:
        if not isinstance(argument, Offset):
            raise TypeError
        if self.fraction == argument.fraction:
            return self._nonnone_displacement() <= argument._nonnone_displacement()
        return self.fraction <= argument.fraction

    def __lt__(self, argument: object) -> bool:
        if not isinstance(argument, Offset):
            raise TypeError
        if self.fraction == argument.fraction:
            return self._nonnone_displacement() < argument._nonnone_displacement()
        return self.fraction < argument.fraction

    def __mod__(self, argument: int | fractions.Fraction) -> Offset:
        fraction = self.fraction % argument
        return Offset(fraction=fraction, displacement=self.displacement)

    def __mul__(self, argument):
        raise NotImplementedError

    def __repr__(self) -> str:
        """
        Gets interpreter representation of offset.

        ..  container:: example

            >>> abjad.Offset(abjad.Fraction(1, 4))
            Offset(Fraction(1, 4))

            >>> duration = abjad.ValueDuration(-1, 16)
            >>> abjad.Offset(abjad.Fraction(1, 4), displacement=duration)
            Offset(Fraction(1, 4), displacement=ValueDuration(numerator=-1, denominator=16))

        """
        string = f"{self.fraction!r}"
        if self.displacement is not None:
            string = string + f", displacement={self.displacement!r}"
        string = f"{Offset.__name__}({string})"
        return string

    __rmul__ = __mul__

    def __str__(self) -> str:
        return str(self.fraction)

    @typing.overload
    def __sub__(self, argument: typing.Self) -> ValueDuration:
        pass

    @typing.overload
    def __sub__(
        self, argument: int | fractions.Fraction | ValueDuration
    ) -> typing.Self:
        pass

    def __sub__(self, argument):
        if isinstance(argument, Offset):
            fraction = self.fraction - argument.fraction
            return ValueDuration(fraction.numerator, fraction.denominator)
        else:
            assert isinstance(argument, ValueDuration), repr(argument)
            result = ValueDuration(*self.fraction.as_integer_ratio()) - argument
            fraction = result.as_fraction()
            return Offset(fraction, displacement=self.displacement)

    def __truediv__(self, argument):
        raise NotImplementedError

    def _nonnone_displacement(self):
        if self.displacement is None:
            return ValueDuration(0)
        return self.displacement

    # TODO: change to as_duration()
    def duration(self) -> ValueDuration:
        """
        Changes offset to duration.

        ..  container:: example

            >>> fraction = abjad.Fraction(1, 4)
            >>> offset = abjad.Offset(fraction)
            >>> offset.duration()
            ValueDuration(numerator=1, denominator=4)

        """
        assert self.displacement is None, repr(self)
        return ValueDuration(*self.fraction.as_integer_ratio())

    def remove_displacement(self):
        """
        Makes new offset equal to this offset without displacement.

        ..  container:: example

            >>> duration = abjad.ValueDuration(-1, 16)
            >>> offset = abjad.Offset(abjad.Fraction(1, 4), displacement=duration)
            >>> offset
            Offset(Fraction(1, 4), displacement=ValueDuration(numerator=-1, denominator=16))

            >>> offset.remove_displacement()
            Offset(Fraction(1, 4))

        """
        return Offset(self.fraction)
