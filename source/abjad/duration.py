"""
Duration, offset, ratio.
"""

from __future__ import annotations

import dataclasses
import fractions
import math
import re
import typing

from . import exceptions as _exceptions
from . import math as _math


def durations(items: list) -> list[Duration]:
    """
    Changes ``items`` to durations.

    ..  container:: example

        >>> abjad.duration.durations([(15, 8), (3, 8), abjad.TimeSignature((3, 4))])
        [Duration(15, 8), Duration(3, 8), Duration(3, 4)]

    """
    durations = []
    for item in items:
        if isinstance(item, tuple):
            duration = Duration(*item)
        elif callable(getattr(item, "duration", None)):
            duration = item.duration()
        else:
            duration = Duration(item)
        durations.append(duration)
    return durations


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


class Duration(fractions.Fraction):
    """
    Duration.

    ..  container:: example

        >>> abjad.Duration(3, 16)
        Duration(3, 16)

    """

    __slots__ = ()

    def __abs__(self) -> typing.Self:
        result = super().__abs__()
        return type(self)(result)

    @typing.overload
    def __add__(self, argument: int | fractions.Fraction) -> typing.Self:
        pass

    @typing.overload
    def __add__(self, argument: float) -> float:
        pass

    @typing.overload
    def __add__(self, argument: complex) -> complex:
        pass

    def __add__(self, argument):
        result = super().__add__(argument)
        if isinstance(result, fractions.Fraction):
            return type(self)(result)
        return result

    @typing.overload
    def __mul__(self, other: int | fractions.Fraction) -> fractions.Fraction:
        pass

    @typing.overload
    def __mul__(self, other: float) -> float:
        pass

    @typing.overload
    def __mul__(self, other: complex) -> complex:
        pass

    def __mul__(self, other):
        if isinstance(other, Duration):
            raise TypeError("Multiplying two durations is undefined")
        result = super().__mul__(other)
        if isinstance(result, fractions.Fraction):
            return type(self)(result)
        return result

    def __neg__(self) -> typing.Self:
        return type(self)(super().__neg__())

    @typing.overload
    def __radd__(self, argument: int | fractions.Fraction) -> typing.Self:
        pass

    @typing.overload
    def __radd__(self, argument: float) -> float:
        pass

    @typing.overload
    def __radd__(self, argument: complex) -> complex:
        pass

    def __radd__(self, argument):
        result = super().__radd__(argument)
        if isinstance(result, fractions.Fraction):
            return type(self)(result)
        return result

    def __repr__(self) -> str:
        return f"{type(self).__name__}({self.numerator}, {self.denominator})"

    @typing.overload
    def __rmul__(self, other: int | fractions.Fraction) -> typing.Self:
        pass

    @typing.overload
    def __rmul__(self, other: float) -> float:
        pass

    @typing.overload
    def __rmul__(self, other: complex) -> complex:
        pass

    def __rmul__(self, argument):
        if isinstance(argument, Duration):
            message = f"Can not multiply two durations: {self}, {argument}"
            raise TypeError(message)
        result = super().__rmul__(argument)
        if isinstance(result, fractions.Fraction):
            return type(self)(result)
        return result

    @typing.overload
    def __rsub__(self, other: int | fractions.Fraction) -> typing.Self:
        pass

    @typing.overload
    def __rsub__(self, other: float) -> float:
        pass

    @typing.overload
    def __rsub__(self, other: complex) -> complex:
        pass

    def __rsub__(self, other):
        result = super().__rsub__(other)
        if isinstance(result, fractions.Fraction):
            return type(self)(result)
        return result

    @typing.overload
    def __rtruediv__(self, other: int | fractions.Fraction) -> fractions.Fraction:
        pass

    @typing.overload
    def __rtruediv__(self, other: float) -> float:
        pass

    @typing.overload
    def __rtruediv__(self, other: complex) -> complex:
        pass

    def __rtruediv__(self, other):
        return super().__rtruediv__(other)

    @typing.overload
    def __sub__(self, other: int | fractions.Fraction) -> typing.Self:
        pass

    @typing.overload
    def __sub__(self, other: float) -> float:
        pass

    @typing.overload
    def __sub__(self, other: complex) -> complex:
        pass

    def __sub__(self, other):
        result = super().__sub__(other)
        if isinstance(result, fractions.Fraction):
            return type(self)(result)
        return result

    @typing.overload
    def __truediv__(self, other: int | fractions.Fraction) -> fractions.Fraction:
        pass

    @typing.overload
    def __truediv__(self, other: float) -> float:
        pass

    @typing.overload
    def __truediv__(self, other: complex) -> complex:
        pass

    def __truediv__(self, other):
        result = super().__truediv__(other)
        if isinstance(other, Duration):
            return fractions.Fraction(self) / fractions.Fraction(other)
        if isinstance(result, fractions.Fraction) and isinstance(other, int):
            return type(self)(result)
        return result

    def clock_string(self) -> str:
        r"""
        Gets clock string.

        ..  container:: example

            >>> abjad.Duration(117).clock_string()
            "1'57''"

        Rounds down to nearest second.
        """
        minutes = int(self / 60)
        seconds = str(int(self - minutes * 60)).zfill(2)
        clock_string = f"{minutes}'{seconds}''"
        return clock_string

    def dot_count(self) -> int:
        r"""
        Gets dot count.

        ..  container:: example

            Dot count defined equal to number of dots required to notate
            duration. Raises assignability error when duration is not
            assignable.

            >>> for n in range(1, 16 + 1):
            ...     try:
            ...         duration = abjad.Duration(n, 16)
            ...         sixteenths = abjad.duration.pair_with_denominator(duration, 16)
            ...         dot_count = duration.dot_count()
            ...         string = f"{sixteenths[0]}/{sixteenths[1]}\t{dot_count}"
            ...         print(string)
            ...     except abjad.AssignabilityError:
            ...         sixteenths = abjad.duration.pair_with_denominator(duration, 16)
            ...         print(f"{sixteenths[0]}/{sixteenths[1]}\t--")
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

    # TODO: port logic to rmakers and then remove
    @staticmethod
    def durations_to_nonreduced_fractions(
        durations: list[Duration],
    ) -> list[tuple[int, int]]:
        """
        Changes ``durations`` to pairs sharing least common denominator.

        ..  container:: example

            >>> items = [abjad.Duration(2, 4), 3, (5, 16)]
            >>> durations = abjad.duration.durations(items)
            >>> result = abjad.Duration.durations_to_nonreduced_fractions(durations)
            >>> for x in result:
            ...     x
            ...
            (8, 16)
            (48, 16)
            (5, 16)

        """
        assert all(isinstance(_, Duration) for _ in durations), repr(durations)
        denominators = [_.denominator for _ in durations]
        lcd = _math.least_common_multiple(*denominators)
        pairs = [pair_with_denominator(_, lcd) for _ in durations]
        return pairs

    # TODO: move to math.py or remove
    def equal_or_greater_assignable(self) -> Duration:
        r"""
        Gets assignable duration equal to or just greater than this duration.

        ..  container:: example

            >>> for numerator in range(1, 16 + 1):
            ...     duration = abjad.Duration(numerator, 16)
            ...     result = duration.equal_or_greater_assignable()
            ...     sixteenths = abjad.duration.pair_with_denominator(duration, 16)
            ...     print(f"{sixteenths[0]}/{sixteenths[1]}\t{result!s}")
            ...
            1/16    1/16
            2/16    1/8
            3/16    3/16
            4/16    1/4
            5/16    3/8
            6/16    3/8
            7/16    7/16
            8/16    1/2
            9/16    3/4
            10/16   3/4
            11/16   3/4
            12/16   3/4
            13/16   7/8
            14/16   7/8
            15/16   15/16
            16/16   1

        """
        good_denominator = _math.greatest_power_of_two_less_equal(self.denominator)
        current_numerator = self.numerator
        candidate = type(self)(current_numerator, good_denominator)
        while not candidate.is_assignable():
            current_numerator += 1
            candidate = type(self)(current_numerator, good_denominator)
        return candidate

    # TODO: move to math.py or remove
    def equal_or_greater_power_of_two(self) -> Duration:
        r"""
        Gets duration equal or just greater power of two.

        ..  container:: example

            >>> for numerator in range(1, 16 + 1):
            ...     duration = abjad.Duration(numerator, 16)
            ...     result = duration.equal_or_greater_power_of_two()
            ...     sixteenths = abjad.duration.pair_with_denominator(duration, 16)
            ...     print(f"{sixteenths[0]}/{sixteenths[1]}\t{result!s}")
            ...
            1/16    1/16
            2/16    1/8
            3/16    1/4
            4/16    1/4
            5/16    1/2
            6/16    1/2
            7/16    1/2
            8/16    1/2
            9/16    1
            10/16   1
            11/16   1
            12/16   1
            13/16   1
            14/16   1
            15/16   1
            16/16   1

        """
        denominator_exponent = -int(math.ceil(math.log(self, 2)))
        return type(self)(fractions.Fraction(1, 2) ** denominator_exponent)

    # TODO: move to math.py or remove
    def equal_or_lesser_assignable(self) -> Duration:
        r"""
        Gets assignable duration equal or just less than this duration.

        ..  container:: example

            >>> for numerator in range(1, 16 + 1):
            ...     duration = abjad.Duration(numerator, 16)
            ...     result = duration.equal_or_lesser_assignable()
            ...     sixteenths = abjad.duration.pair_with_denominator(duration, 16)
            ...     print(f"{sixteenths[0]}/{sixteenths[1]}\t{result!s}")
            ...
            1/16    1/16
            2/16    1/8
            3/16    3/16
            4/16    1/4
            5/16    1/4
            6/16    3/8
            7/16    7/16
            8/16    1/2
            9/16    1/2
            10/16   1/2
            11/16   1/2
            12/16   3/4
            13/16   3/4
            14/16   7/8
            15/16   15/16
            16/16   1

        """
        good_denominator = 2 ** (int(math.ceil(math.log(self.denominator, 2))) + 0)
        current_numerator = self.numerator
        candidate = type(self)(current_numerator, good_denominator)
        while not candidate.is_assignable():
            current_numerator -= 1
            candidate = type(self)(current_numerator, good_denominator)
        return candidate

    # TODO: move to math.py or remove
    def equal_or_lesser_power_of_two(self) -> Duration:
        r"""
        Gets duration of the form ``d**2`` equal to or just less than this
        duration.

        ..  container:: example

            >>> for numerator in range(1, 16 + 1):
            ...     duration = abjad.Duration(numerator, 16)
            ...     result = duration.equal_or_lesser_power_of_two()
            ...     sixteenths = abjad.duration.pair_with_denominator(duration, 16)
            ...     print(f"{sixteenths[0]}/{sixteenths[1]}\t{result!s}")
            ...
            1/16    1/16
            2/16    1/8
            3/16    1/8
            4/16    1/4
            5/16    1/4
            6/16    1/4
            7/16    1/4
            8/16    1/2
            9/16    1/2
            10/16   1/2
            11/16   1/2
            12/16   1/2
            13/16   1/2
            14/16   1/2
            15/16   1/2
            16/16   1

        """
        return type(self)(fractions.Fraction(1, 2) ** self.exponent())

    def exponent(self) -> int:
        r"""
        Gets base-2 exponent.

        ..  container:: example

            >>> for numerator in range(1, 16 + 1):
            ...     duration = abjad.Duration(numerator, 16)
            ...     exponent = duration.exponent()
            ...     sixteenths = abjad.duration.pair_with_denominator(duration, 16)
            ...     print(f"{sixteenths[0]}/{sixteenths[1]}\t{duration.exponent()!s}")
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
            ...     duration = abjad.Duration(n, 64)
            ...     sixty_fourths = abjad.duration.pair_with_denominator(duration, 64)
            ...     print(f"{sixty_fourths[0]}/{sixty_fourths[1]}\t{duration.flag_count()}")
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

    def fraction(self):
        """
        Returns duration as fraction.
        """
        return fractions.Fraction(self)

    @staticmethod
    def from_clock_string(clock_string) -> Duration:
        """
        Initializes duration (in seconds) from ``clock_string``.

        ..  container:: example

            >>> abjad.Duration.from_clock_string("0'00''")
            Duration(0, 1)

            >>> abjad.Duration.from_clock_string("0'59''")
            Duration(59, 1)

            >>> abjad.Duration.from_clock_string("1'00''")
            Duration(60, 1)

            >>> abjad.Duration.from_clock_string("1'17''")
            Duration(77, 1)

        """
        minutes = 0
        if "'" in clock_string:
            tick_index = clock_string.find("'")
            minutes = clock_string[:tick_index]
            minutes = int(minutes)
        seconds = clock_string[-4:-2]
        seconds = int(seconds)
        seconds = 60 * minutes + seconds
        return Duration(seconds)

    @staticmethod
    def from_dot_count(dot_count: int) -> Duration:
        """
        Initializes duration from ``dot_count``.

        ..  container::

            >>> abjad.Duration.from_dot_count(2)
            Duration(7, 4)

        """
        assert isinstance(dot_count, int), repr(dot_count)
        assert 0 <= dot_count, repr(dot_count)
        denominator = 2**dot_count
        numerator = 2 ** (dot_count + 1) - 1
        duration = Duration(numerator, denominator)
        return duration

    @staticmethod
    def from_lilypond_duration_string(lilypond_duration_string: str) -> Duration:
        """
        Initializes duration from LilyPond duration string.

        ..  container:: example

            >>> abjad.Duration.from_lilypond_duration_string("8.")
            Duration(3, 16)

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
        return Duration(rational)

    def is_assignable(self) -> bool:
        r"""
        Is true when duration is assignable.

        ..  container:: example

            >>> for numerator in range(0, 16 + 1):
            ...     duration = abjad.Duration(numerator, 16)
            ...     sixteenths = abjad.duration.pair_with_denominator(duration, 16)
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
        if 0 < self < 16:
            if _math.is_nonnegative_integer_power_of_two(self.denominator):
                if _math.is_assignable_integer(self.numerator):
                    return True
        return False

    def is_dyadic(self) -> bool:
        r"""
        Is true when denominator of duration is integer power of two.

        ..  container:: example

            >>> for n in range(1, 16 + 1):
            ...     duration = abjad.Duration(1, n)
            ...     print(f"{duration!s}\t{duration.is_dyadic()}")
            ...
            1       True
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

    # TODO: move logic to parser.py and then remove
    @staticmethod
    def is_token(argument) -> bool:
        """
        Is true when ``argument`` correctly initializes a duration.

        ..  container:: example

            >>> abjad.Duration.is_token('8.')
            True

        """
        try:
            Duration.__new__(Duration, argument)
            return True
        except Exception:
            return False

    def lilypond_duration_string(self) -> str:
        """
        Gets LilyPond duration string.

        ..  container:: example

            >>> abjad.Duration(3, 16).lilypond_duration_string()
            '8.'

        """
        if not self.is_assignable():
            raise _exceptions.AssignabilityError(self)
        undotted_rational = self.equal_or_lesser_power_of_two()
        if undotted_rational <= 1:
            undotted_duration_string = str(undotted_rational.denominator)
        elif undotted_rational == type(self)(2, 1):
            undotted_duration_string = r"\breve"
        elif undotted_rational == type(self)(4, 1):
            undotted_duration_string = r"\longa"
        elif undotted_rational == type(self)(8, 1):
            undotted_duration_string = r"\maxima"
        else:
            raise ValueError(f"can not process undotted rational: {undotted_rational}")
        dot_count = self.dot_count()
        dot_string = "." * dot_count
        dotted_duration_string = undotted_duration_string + dot_string
        return dotted_duration_string

    def pair(self) -> tuple[int, int]:
        """
        Gets numerator and denominator pair.

        ..  container:: example

            >>> abjad.Duration(3, 16).pair()
            (3, 16)

        """
        return self.numerator, self.denominator

    def reciprocal(self) -> Duration:
        """
        Gets reciprocal.

        ..  container:: example

            >>> abjad.Duration(3, 7).reciprocal()
            Duration(7, 3)

        """
        return type(self)(self.denominator, self.numerator)


class Offset(Duration):
    """
    Offset.

    ..  container:: example

        >>> abjad.Offset(3, 16)
        Offset(3, 16)

        >>> abjad.Offset(3, 16, displacement=abjad.Duration(-1, 16))
        Offset(3, 16, displacement=Duration(-1, 16))

    """

    __slots__ = ("_displacement",)

    _displacement: Duration | None

    def __new__(
        class_,
        numerator=0,
        denominator=None,
        *,
        displacement: Duration | None = None,
    ) -> Offset:
        self = super().__new__(class_, numerator, denominator)
        if displacement is None and isinstance(numerator, Offset):
            displacement = numerator.displacement()
        if displacement is not None:
            assert isinstance(displacement, Duration), repr(displacement)
        self._displacement = displacement
        return self

    def __copy__(self) -> Offset:
        return type(self)(*self.pair(), displacement=self.displacement())

    def __deepcopy__(self, memo) -> Offset:
        return self.__copy__()

    def __eq__(self, argument: object) -> bool:
        if isinstance(argument, type(self)) and self.pair() == argument.pair():
            return (
                self._get_nonnone_displacement() == argument._get_nonnone_displacement()
            )
        return super().__eq__(argument)

    def __ge__(self, argument) -> bool:
        if isinstance(argument, type(self)) and self.pair() == argument.pair():
            return (
                self._get_nonnone_displacement() >= argument._get_nonnone_displacement()
            )
        return super().__ge__(argument)

    def __gt__(self, argument) -> bool:
        if isinstance(argument, type(self)) and self.pair() == argument.pair():
            return (
                self._get_nonnone_displacement() > argument._get_nonnone_displacement()
            )
        return Duration.__gt__(self, argument)

    @typing.no_type_check
    def __hash__(self) -> int:
        return hash((self.pair(), self._get_nonnone_displacement()))

    def __le__(self, argument) -> bool:
        if isinstance(argument, type(self)) and self.pair() == argument.pair():
            return (
                self._get_nonnone_displacement() <= argument._get_nonnone_displacement()
            )
        return super().__le__(argument)

    def __lt__(self, argument) -> bool:
        if isinstance(argument, type(self)) and self.pair() == argument.pair():
            return (
                self._get_nonnone_displacement() < argument._get_nonnone_displacement()
            )
        return super().__lt__(argument)

    def __repr__(self) -> str:
        """
        Gets interpreter representation of offset.

        ..  container:: example

            >>> abjad.Offset(1, 4)
            Offset(1, 4)

            >>> abjad.Offset(1, 4, displacement=abjad.Duration(-1, 16))
            Offset(1, 4, displacement=Duration(-1, 16))

        """
        n, d = self.numerator, self.denominator
        if self.displacement() is None:
            return f"{type(self).__name__}({n}, {d})"
        else:
            string = f"{n}, {d}, displacement={self.displacement()!r}"
            return f"{type(self).__name__}({string})"

    def __sub__(self, argument):
        if isinstance(argument, type(self)):
            return Duration(super().__sub__(argument))
        elif isinstance(argument, Duration):
            return super().__sub__(argument)
        else:
            argument = type(self)(argument)
            return self - argument

    def _get_nonnone_displacement(self):
        if self.displacement() is None:
            return Duration(0)
        return self.displacement()

    def displacement(self):
        """
        Gets displacement.

        ..  container:: example

            >>> abjad.Offset(1, 4).displacement() is None
            True

            >>> abjad.Offset(1, 4, displacement=abjad.Duration(-1, 16)).displacement()
            Duration(-1, 16)

        """
        return self._displacement

    def value_offset(self) -> ValueOffset:
        """
        Gets offset as value offset.

        ..  container:: example

            >>> offset = abjad.Offset(3, 16)
            >>> offset.value_offset()
            ValueOffset(fraction=Fraction(3, 16), displacement=None)

        """
        return ValueOffset.from_offset(self)


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

    # TODO: rename to fraction()
    def as_fraction(self):
        """
        Changes (unreduced) ratio to (reduced) fraction.

        ..  container:: example

            >>> abjad.Ratio(6, 4).as_fraction()
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
        fraction = self.as_fraction()
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
class ValueOffset:
    """
    Value offset.

    ..  container:: example

        >>> fraction = abjad.Fraction(3, 16)
        >>> abjad.ValueOffset(fraction)
        ValueOffset(fraction=Fraction(3, 16), displacement=None)

        >>> displacement = abjad.Duration(-1, 16)
        >>> abjad.ValueOffset(fraction, displacement=displacement)
        ValueOffset(fraction=Fraction(3, 16), displacement=Duration(-1, 16))

    """

    fraction: fractions.Fraction
    displacement: Duration | None = None

    def __post_init__(self):
        assert isinstance(self.fraction, fractions.Fraction), repr(self.fraction)
        if self.displacement is not None:
            assert isinstance(self.displacement, Duration), repr(self.displacement)

    def __add__(self, argument: int | fractions.Fraction | Duration) -> ValueOffset:
        assert isinstance(argument, int | fractions.Fraction | Duration), repr(argument)
        if isinstance(argument, Duration):
            fraction = argument.fraction()
        else:
            fraction = fractions.Fraction(argument)
        offset = ValueOffset(self.fraction + fraction, displacement=self.displacement)
        return offset

    def __radd__(self, argument: int | fractions.Fraction | Duration) -> ValueOffset:
        assert isinstance(argument, int | fractions.Fraction | Duration), repr(argument)
        if isinstance(argument, Duration):
            fraction = argument.fraction()
        else:
            fraction = fractions.Fraction(argument)
        offset = ValueOffset(fraction + self.fraction, displacement=self.displacement)
        return offset

    def __eq__(self, argument: object) -> bool:
        if isinstance(argument, type(self)):
            if self.fraction == argument.fraction:
                if self._nonnone_displacement() == argument._nonnone_displacement():
                    return True
        return False

    def __ge__(self, argument) -> bool:
        if not isinstance(argument, type(self)):
            raise TypeError
        if self.fraction == argument.fraction:
            return self._nonnone_displacement() >= argument._nonnone_displacement()
        return self.fraction >= argument.fraction

    def __gt__(self, argument) -> bool:
        if not isinstance(argument, type(self)):
            raise TypeError
        if self.fraction == argument.fraction:
            return self._nonnone_displacement() > argument._nonnone_displacement()
        return self.fraction > argument.fraction

    def __le__(self, argument) -> bool:
        if not isinstance(argument, type(self)):
            raise TypeError
        if self.fraction == argument.fraction:
            return self._nonnone_displacement() <= argument._nonnone_displacement()
        return self.fraction <= argument.fraction

    def __lt__(self, argument) -> bool:
        if not isinstance(argument, type(self)):
            raise TypeError
        if self.fraction == argument.fraction:
            return self._nonnone_displacement() < argument._nonnone_displacement()
        return self.fraction < argument.fraction

    def __mul__(self, argument):
        raise NotImplementedError

    __rmul__ = __mul__

    def __str__(self) -> str:
        return str(self.fraction)

    @typing.overload
    def __sub__(self, argument: typing.Self) -> Duration:
        pass

    @typing.overload
    def __sub__(self, argument: int | fractions.Fraction | Duration) -> typing.Self:
        pass

    def __sub__(self, argument):
        if isinstance(argument, type(self)):
            fraction = self.fraction - argument.fraction
            return Duration(fraction.numerator, fraction.denominator)
        else:
            assert isinstance(argument, int | fractions.Fraction | Duration), repr(
                argument
            )
            fraction = self.fraction - argument
            return ValueOffset(
                fraction,
                # TODO: uncomment
                # displacement=self.displacement,
            )

    def __truediv__(self, argument):
        raise NotImplementedError

    def _nonnone_displacement(self):
        if self.displacement is None:
            return Duration(0)
        return self.displacement

    @staticmethod
    def from_offset(offset: Offset) -> ValueOffset:
        """
        Makes value offset from ``offset``.
        """
        fraction = fractions.Fraction(*offset.pair())
        value_offset = ValueOffset(fraction, displacement=offset.displacement())
        assert value_offset.displacement == offset.displacement()
        return value_offset

    def offset(self) -> Offset:
        """
        Makes offset from value offset.
        """
        return Offset(self.fraction, displacement=self.displacement)
