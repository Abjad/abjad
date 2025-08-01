"""
Duration, offset, ratio.
"""

import dataclasses
import fractions
import math
import re
import typing

from . import exceptions as _exceptions
from . import math as _math


class Duration(fractions.Fraction):
    """
    Duration.

    ..  container:: example

        Initializes from integer numerator:

        >>> abjad.Duration(3)
        Duration(3, 1)

        Initializes from integer numerator and denominator:

        >>> abjad.Duration(3, 16)
        Duration(3, 16)

        Initializes from integer-equivalent numeric numerator:

        >>> abjad.Duration(3.0)
        Duration(3, 1)

        Initializes from integer-equivalent numeric numerator and denominator:

        >>> abjad.Duration(3.0, 16)
        Duration(3, 16)

        Initializes from integer-equivalent singleton:

        >>> abjad.Duration((3,))
        Duration(3, 1)

        Initializes from integer-equivalent pair:

        >>> abjad.Duration((3, 16))
        Duration(3, 16)

        Initializes from other duration:

        >>> abjad.Duration(abjad.Duration(3, 16))
        Duration(3, 16)

        Intializes from fraction:

        >>> import fractions
        >>> abjad.Duration(fractions.Fraction(3, 16))
        Duration(3, 16)

        Initializes from solidus string:

        >>> abjad.Duration("3/16")
        Duration(3, 16)

    ..  container:: example

        Durations inherit from built-in fraction:

        >>> isinstance(abjad.Duration(3, 16), fractions.Fraction)
        True

    ..  container:: example

        Durations are numbers:

        >>> import numbers

        >>> isinstance(abjad.Duration(3, 16), numbers.Number)
        True

    """

    __slots__ = ()

    # dummy initializer so that mypy knows about _denominator, _numerator
    def __init__(self, *arguments):
        self._denominator = self._denominator
        self._numerator = self._numerator
        return None

    def __new__(class_, *arguments):
        """
        Makes new duration.
        """
        if len(arguments) == 1:
            argument = arguments[0]
            if type(argument) is class_:
                return argument
            try:
                return fractions.Fraction.__new__(class_, *argument)
            except (AttributeError, TypeError):
                pass
            try:
                return fractions.Fraction.__new__(class_, argument)
            except (AttributeError, TypeError):
                pass
            if callable(hasattr(argument, "duration")):
                return argument.duration()
            if (
                isinstance(argument, tuple)
                and len(argument) == 2
                and _math.is_integer_equivalent(argument[0])
                and _math.is_integer_equivalent(argument[1])
                and not argument[1] == 0
            ):
                return fractions.Fraction.__new__(
                    class_, int(argument[0]), int(argument[1])
                )
            if hasattr(argument, "duration"):
                try:
                    return fractions.Fraction.__new__(class_, argument.duration)
                except TypeError:
                    pass
                return fractions.Fraction.__new__(class_, argument.duration())
            if isinstance(argument, str) and "/" not in argument:
                result = Duration._initialize_from_lilypond_duration_string(argument)
                return fractions.Fraction.__new__(class_, result)
            if (
                isinstance(argument, tuple)
                and len(argument) == 1
                and _math.is_integer_equivalent(argument[0])
            ):
                return fractions.Fraction.__new__(class_, int(argument[0]))
        else:
            try:
                return fractions.Fraction.__new__(class_, *arguments)
            except TypeError:
                pass
            if _math.all_are_integer_equivalent_numbers(arguments):
                return fractions.Fraction.__new__(class_, *[int(x) for x in arguments])
        raise ValueError(f"can not construct duration: {arguments!r}.")

    def __abs__(self, *arguments):
        """
        Gets absolute value of duration.

        Returns nonnegative duration.
        """
        return type(self)(fractions.Fraction.__abs__(self, *arguments))

    def __add__(self, *arguments):
        """
        Adds duration to ``arguments``.

        ..  container:: example

            Returns duration when ``arguments`` is a duration:

            >>> duration_1 = abjad.Duration(1, 2)
            >>> duration_2 = abjad.Duration(3, 2)
            >>> duration_1 + duration_2
            Duration(2, 1)

        Returns duration.
        """
        result = type(self)(fractions.Fraction.__add__(self, *arguments))
        return result

    def __div__(self, *arguments) -> fractions.Fraction:
        """
        Divides duration by ``arguments``.

        ..  container:: example

            >>> abjad.Duration(1) / abjad.Duration(3, 3)
            Fraction(1, 1)

        """
        if len(arguments) == 1 and isinstance(arguments[0], type(self)):
            fraction = fractions.Fraction.__truediv__(self, *arguments)
            result = fractions.Fraction(fraction)
        else:
            result = type(self)(fractions.Fraction.__truediv__(self, *arguments))
        return result

    def __divmod__(self, *arguments):
        """
        Equals the pair (duration // ``arguments``, duration % ``arguments``).

        Returns pair.
        """
        truncated, residue = fractions.Fraction.__divmod__(self, *arguments)
        truncated = type(self)(truncated)
        residue = type(self)(residue)
        return truncated, residue

    def __eq__(self, argument) -> bool:
        """
        Is true when duration equals ``argument``.
        """
        return fractions.Fraction.__eq__(self, argument)

    def __ge__(self, argument) -> bool:
        """
        Is true when duration is greater than or equal to ``argument``.
        """
        return fractions.Fraction.__ge__(self, argument)

    def __gt__(self, argument) -> bool:
        """
        Is true when duration is greater than ``argument``.
        """
        return fractions.Fraction.__gt__(self, argument)

    @typing.no_type_check
    def __hash__(self) -> int:
        """
        Hashes duration.
        """
        return super().__hash__()

    def __le__(self, argument) -> bool:
        """
        Is true when duration is less than or equal to ``argument``.
        """
        return fractions.Fraction.__le__(self, argument)

    def __lt__(self, argument) -> bool:
        """
        Is true when duration is less than ``argument``.
        """
        return fractions.Fraction.__lt__(self, argument)

    def __mod__(self, *arguments):
        """
        Modulus operator applied to duration.

        Returns duration.
        """
        return type(self)(fractions.Fraction.__mod__(self, *arguments))

    def __mul__(self, argument):
        """
        Duration multiplied by ``argument``.

        ..  container:: example

            Returns a new duration when ``argument`` is a duration:

            >>> duration_1 = abjad.Duration(1, 2)
            >>> duration_2 = abjad.Duration(3, 2)
            >>> duration_1 * duration_2
            Duration(3, 4)

        Returns duration.
        """
        result = type(self)(fractions.Fraction.__mul__(self, argument))
        return result

    def __ne__(self, argument) -> bool:
        """
        Redefined explicitly because ``abjad.Duration`` inherits from built-in
        ``fractions.Fraction``:

        "The __ne__ method follows automatically from __eq__ only if __ne__
        isn't already defined in a superclass.  So, if you're inheriting from a
        builtin, it's best to override both."

        See https://bugs.python.org/issue4395#msg89533.

        ..  container:: example

            REGRESSION:

            >>> offset_1 = abjad.Offset(1)
            >>> offset_2 = abjad.Offset(1, displacement=(-1, 16))

            >>> offset_1 == offset_2
            False

            >>> offset_1 != offset_2
            True

        """
        return not self == argument

    def __neg__(self, *arguments):
        """
        Negates duration.

        Returns new duration.
        """
        return type(self)(fractions.Fraction.__neg__(self, *arguments))

    def __pos__(self, *arguments):
        """
        Get positive duration.

        Returns new duration.
        """
        return type(self)(fractions.Fraction.__pos__(self, *arguments))

    def __pow__(self, *arguments):
        """
        Raises duration to ``arguments`` power.

        Returns new duration.
        """
        return type(self)(fractions.Fraction.__pow__(self, *arguments))

    def __radd__(self, *arguments):
        """
        Adds ``arguments`` to duration.

        Returns new duration.
        """
        return type(self)(fractions.Fraction.__radd__(self, *arguments))

    def __rdiv__(self, *arguments):
        """
        Divides ``arguments`` by duration.

        Returns new duration.
        """
        return type(self)(fractions.Fraction.__rdiv__(self, *arguments))

    def __rdivmod__(self, *arguments):
        """
        Documentation required.
        """
        return type(self)(fractions.Fraction.__rdivmod__(self, *arguments))

    def __reduce__(self):
        """
        Documentation required.
        """
        return type(self), (self.numerator, self.denominator)

    def __reduce_ex__(self, protocol):
        """
        Documentation required.
        """
        return type(self), (self.numerator, self.denominator)

    def __repr__(self) -> str:
        """
        Gets repr.
        """
        return f"{type(self).__name__}({self.numerator}, {self.denominator})"

    def __rmod__(self, *arguments):
        """
        Documentation required.
        """
        return type(self)(fractions.Fraction.__rmod__(self, *arguments))

    def __rmul__(self, *arguments):
        """
        Multiplies ``arguments`` by duration.

        Returns new duration.
        """
        return type(self)(fractions.Fraction.__rmul__(self, *arguments))

    def __rpow__(self, *arguments):
        """
        Raises ``arguments`` to the power of duration.

        Returns new duration.
        """
        return type(self)(fractions.Fraction.__rpow__(self, *arguments))

    def __rsub__(self, *arguments):
        """
        Subtracts duration from ``arguments``.

        Returns new duration.
        """
        return type(self)(fractions.Fraction.__rsub__(self, *arguments))

    def __rtruediv__(self, *arguments):
        """
        Documentation required.

        Returns new duration.
        """
        return type(self)(fractions.Fraction.__rtruediv__(self, *arguments))

    def __sub__(self, *arguments):
        """
        Subtracts ``arguments`` from duration.

        ..  container:: example

            >>> abjad.Duration(1, 2) - abjad.Duration(2, 8)
            Duration(1, 4)

        Returns new duration.
        """
        return type(self)(fractions.Fraction.__sub__(self, *arguments))

    def __truediv__(self, *arguments):
        """
        Documentation required.
        """
        return self.__div__(*arguments)

    @staticmethod
    def _initialize_from_lilypond_duration_string(duration_string):
        numeric_body_strings = [str(2**n) for n in range(8)]
        other_body_strings = [r"\\breve", r"\\longa", r"\\maxima"]
        body_strings = numeric_body_strings + other_body_strings
        body_strings = "|".join(body_strings)
        pattern = r"^(%s)(\.*)$" % body_strings
        match = re.match(pattern, duration_string)
        if match is None:
            raise TypeError(f"incorrect duration string format: {duration_string!r}.")
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
        return rational

    @staticmethod
    def _least_power_of_two_greater_equal(n, i=0) -> int:
        """
        When ``i = 2``, returns the second integer power of 2 greater than
        the least integer power of 2 greater than or equal to ``n``, and, in
        general, return the ``i`` th integer power of 2 greater than the least
        integer power of 2 greater than or equal to ``n``.
        """
        assert isinstance(n, int | float | fractions.Fraction), repr(n)
        assert 0 <= n, repr(n)
        result = 2 ** (int(math.ceil(math.log(n, 2))) + i)
        return result

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
            ...         sixteenths = abjad.duration.with_denominator(duration, 16)
            ...         dot_count = duration.dot_count()
            ...         string = f"{sixteenths[0]}/{sixteenths[1]}\t{dot_count}"
            ...         print(string)
            ...     except abjad.AssignabilityError:
            ...         sixteenths = abjad.duration.with_denominator(duration, 16)
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

    @staticmethod
    def durations_to_nonreduced_fractions(durations: list) -> list[tuple[int, int]]:
        """
        Changes ``durations`` to pairs sharing least common denominator.

        ..  container:: example

            >>> durations = [abjad.Duration(2, 4), 3, (5, 16)]
            >>> result = abjad.Duration.durations_to_nonreduced_fractions(durations)
            >>> for x in result:
            ...     x
            ...
            (8, 16)
            (48, 16)
            (5, 16)

        """
        durations_ = [Duration(_) for _ in durations]
        denominators = [_.denominator for _ in durations_]
        lcd = _math.least_common_multiple(*denominators)
        pairs = [with_denominator(_, lcd) for _ in durations_]
        return pairs

    def equal_or_greater_assignable(self) -> "Duration":
        r"""
        Gets assignable duration equal to or just greater than this duration.

        ..  container:: example

            >>> for numerator in range(1, 16 + 1):
            ...     duration = abjad.Duration(numerator, 16)
            ...     result = duration.equal_or_greater_assignable()
            ...     sixteenths = abjad.duration.with_denominator(duration, 16)
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

    def equal_or_greater_power_of_two(self) -> "Duration":
        r"""
        Gets duration equal or just greater power of two.

        ..  container:: example

            >>> for numerator in range(1, 16 + 1):
            ...     duration = abjad.Duration(numerator, 16)
            ...     result = duration.equal_or_greater_power_of_two()
            ...     sixteenths = abjad.duration.with_denominator(duration, 16)
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
        return type(self)(1, 2) ** denominator_exponent

    def equal_or_lesser_assignable(self) -> "Duration":
        r"""
        Gets assignable duration equal or just less than this duration.

        ..  container:: example

            >>> for numerator in range(1, 16 + 1):
            ...     duration = abjad.Duration(numerator, 16)
            ...     result = duration.equal_or_lesser_assignable()
            ...     sixteenths = abjad.duration.with_denominator(duration, 16)
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
        good_denominator = self._least_power_of_two_greater_equal(self.denominator)
        current_numerator = self.numerator
        candidate = type(self)(current_numerator, good_denominator)
        while not candidate.is_assignable():
            current_numerator -= 1
            candidate = type(self)(current_numerator, good_denominator)
        return candidate

    def equal_or_lesser_power_of_two(self) -> "Duration":
        r"""
        Gets duration of the form ``d**2`` equal to or just less than this
        duration.

        ..  container:: example

            >>> for numerator in range(1, 16 + 1):
            ...     duration = abjad.Duration(numerator, 16)
            ...     result = duration.equal_or_lesser_power_of_two()
            ...     sixteenths = abjad.duration.with_denominator(duration, 16)
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
        return type(self)(1, 2) ** self.exponent()

    def exponent(self) -> int:
        r"""
        Gets base-2 exponent.

        ..  container:: example

            >>> for numerator in range(1, 16 + 1):
            ...     duration = abjad.Duration(numerator, 16)
            ...     exponent = duration.exponent()
            ...     sixteenths = abjad.duration.with_denominator(duration, 16)
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
            ...     sixty_fourths = abjad.duration.with_denominator(duration, 64)
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

    @staticmethod
    def from_clock_string(clock_string) -> "Duration":
        """
        Initializes duration (in seconds) from clock string.

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
    def from_lilypond_duration_string(
        lilypond_duration_string,
    ) -> "Duration":
        """
        Initializes duration from LilyPond duration string.

        ..  container:: example

            >>> abjad.Duration.from_lilypond_duration_string('8.')
            Duration(3, 16)

        """
        fraction = Duration._initialize_from_lilypond_duration_string(
            lilypond_duration_string
        )
        return Duration(fraction)

    def is_assignable(self) -> bool:
        r"""
        Is true when duration is assignable.

        ..  container:: example

            >>> for numerator in range(0, 16 + 1):
            ...     duration = abjad.Duration(numerator, 16)
            ...     sixteenths = abjad.duration.with_denominator(duration, 16)
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

            Raises assignability error when duration is not assignable.

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

    def reciprocal(self) -> "Duration":
        """
        Gets reciprocal.

        ..  container:: example

            >>> abjad.Duration(3, 7).reciprocal()
            Duration(7, 3)

        """
        return type(self)(self.denominator, self.numerator)

    def to_clock_string(self) -> str:
        r"""
        Changes duration to clock string.

        ..  container:: example

            Rounds down to nearest second.

            >>> note = abjad.Note("c'4")
            >>> duration = abjad.Duration(117)
            >>> clock_string = duration.to_clock_string()
            >>> clock_string
            "1'57''"

            >>> string = rf"\markup {{ {clock_string} }}"
            >>> markup = abjad.Markup(string)
            >>> abjad.attach(markup, note, direction=abjad.UP)
            >>> abjad.show(note) # doctest: +SKIP

            ..  docs::

                >>> string = abjad.lilypond(note)
                >>> print(string)
                c'4
                ^ \markup { 1'57'' }

        """
        minutes = int(self / 60)
        seconds = str(int(self - minutes * 60)).zfill(2)
        clock_string = f"{minutes}'{seconds}''"
        return clock_string


class Offset(Duration):
    """
    Offset.

    ..  container:: example

        Initializes from integer numerator:

        >>> abjad.Offset(3)
        Offset((3, 1))

        Initializes from integer numerator and denominator:

        >>> abjad.Offset(3, 16)
        Offset((3, 16))

        Initializes from integer-equivalent numeric numerator:

        >>> abjad.Offset(3.0)
        Offset((3, 1))

        Initializes from integer-equivalent numeric numerator and denominator:

        >>> abjad.Offset(3.0, 16)
        Offset((3, 16))

        Initializes from integer-equivalent singleton:

        >>> abjad.Offset((3,))
        Offset((3, 1))

        Initializes from integer-equivalent pair:

        >>> abjad.Offset((3, 16))
        Offset((3, 16))

        Initializes from duration:

        >>> abjad.Offset(abjad.Duration(3, 16))
        Offset((3, 16))

        Initializes from other offset:

        >>> abjad.Offset(abjad.Offset(3, 16))
        Offset((3, 16))

        Initializes from other offset with displacement:

        >>> offset = abjad.Offset((3, 16), displacement=(-1, 16))
        >>> abjad.Offset(offset)
        Offset((3, 16), displacement=Duration(-1, 16))

        Intializes from fraction:

        >>> import fractions
        >>> abjad.Offset(fractions.Fraction(3, 16))
        Offset((3, 16))

        Initializes from solidus string:

        >>> abjad.Offset("3/16")
        Offset((3, 16))

    ..  container:: example

        Offsets inherit from built-in fraction:

        >>> isinstance(abjad.Offset(3, 16), fractions.Fraction)
        True

    ..  container:: example

        Offsets are numbers:

        >>> import numbers

        >>> isinstance(abjad.Offset(3, 16), numbers.Number)
        True

    """

    __slots__ = ("_displacement",)

    # dummy initializer so that mypy knows about _denominator, _displacement, _numerator
    def __init__(self, *arguments, **keywords):
        self._denominator = self._denominator
        self._displacement = self._displacement
        self._numerator = self._numerator
        return None

    def __new__(class_, *arguments, **keywords):
        displacement = None
        for argument in arguments:
            try:
                displacement = argument.displacement()
                break
            except AttributeError:
                pass
        displacement = displacement or keywords.get("displacement")
        if displacement is not None:
            displacement = Duration(displacement)
        displacement = displacement or None
        if len(arguments) == 1 and isinstance(arguments[0], Duration):
            arguments = arguments[0].pair()
        self = Duration.__new__(class_, *arguments)
        self._displacement = displacement
        return self

    def __copy__(self, *arguments) -> "Offset":
        """
        Copies offset.

        >>> import copy

        ..  container:: example

            Copies offset with displacement:

            >>> offset_1 = abjad.Offset((1, 4), displacement=(-1, 16))
            >>> offset_2 = copy.copy(offset_1)

            >>> offset_1
            Offset((1, 4), displacement=Duration(-1, 16))

            >>> offset_2
            Offset((1, 4), displacement=Duration(-1, 16))

            >>> offset_1 == offset_2
            True

            >>> offset_1 is offset_2
            False

        """
        return type(self)(self.pair(), displacement=self.displacement())

    def __deepcopy__(self, *arguments) -> "Offset":
        """
        Deep copies offset.

        >>> import copy

        ..  container:: example

            Copies offset with displacement:

            >>> offset_1 = abjad.Offset((1, 4), displacement=(-1, 16))
            >>> offset_2 = copy.deepcopy(offset_1)

            >>> offset_1
            Offset((1, 4), displacement=Duration(-1, 16))

            >>> offset_2
            Offset((1, 4), displacement=Duration(-1, 16))

            >>> offset_1 == offset_2
            True

            >>> offset_1 is offset_2
            False

        """
        return self.__copy__(*arguments)

    def __eq__(self, argument) -> bool:
        """
        Is true when offset equals ``argument``.

        ..  container:: example

            With equal numerators, denominators and displacement:

            >>> offset_1 = abjad.Offset((1, 4), displacement=(-1, 16))
            >>> offset_2 = abjad.Offset((1, 4), displacement=(-1, 16))

            >>> offset_1 == offset_1
            True
            >>> offset_1 == offset_2
            True
            >>> offset_2 == offset_1
            True
            >>> offset_2 == offset_2
            True

        ..  container:: example

            With equal numerators and denominators but differing grace
            displacements:

            >>> offset_1 = abjad.Offset((1, 4), displacement=(-1, 8))
            >>> offset_2 = abjad.Offset((1, 4), displacement=(-1, 16))

            >>> offset_1 == offset_1
            True
            >>> offset_1 == offset_2
            False
            >>> offset_2 == offset_1
            False
            >>> offset_2 == offset_2
            True

        ..  container:: example

            With differing numerators and denominators. Ignores grace
            displacements:

            >>> offset_1 = abjad.Offset((1, 4))
            >>> offset_2 = abjad.Offset((1, 2), displacement=(-99))

            >>> offset_1 == offset_1
            True
            >>> offset_1 == offset_2
            False
            >>> offset_2 == offset_1
            False
            >>> offset_2 == offset_2
            True

        """
        if isinstance(argument, type(self)) and self.pair() == argument.pair():
            return self._get_displacement() == argument._get_displacement()
        return super().__eq__(argument)

    def __ge__(self, argument) -> bool:
        """
        Is true when offset is greater than or equal to ``argument``.

        ..  container:: example

            With equal numerators, denominators and displacement:

            >>> offset_1 = abjad.Offset((1, 4), displacement=(-1, 16))
            >>> offset_2 = abjad.Offset((1, 4), displacement=(-1, 16))

            >>> offset_1 >= offset_1
            True
            >>> offset_1 >= offset_2
            True
            >>> offset_2 >= offset_1
            True
            >>> offset_2 >= offset_2
            True

        ..  container:: example

            With equal numerators and denominators but differing grace
            displacements:

            >>> offset_1 = abjad.Offset((1, 4), displacement=(-1, 8))
            >>> offset_2 = abjad.Offset((1, 4), displacement=(-1, 16))

            >>> offset_1 >= offset_1
            True
            >>> offset_1 >= offset_2
            False
            >>> offset_2 >= offset_1
            True
            >>> offset_2 >= offset_2
            True

        ..  container:: example

            With differing numerators and denominators. Ignores grace
            displacements:

            >>> offset_1 = abjad.Offset((1, 4))
            >>> offset_2 = abjad.Offset((1, 2), displacement=(-99))

            >>> offset_1 >= offset_1
            True
            >>> offset_1 >= offset_2
            False
            >>> offset_2 >= offset_1
            True
            >>> offset_2 >= offset_2
            True

        """
        if isinstance(argument, type(self)) and self.pair() == argument.pair():
            return self._get_displacement() >= argument._get_displacement()
        return super().__ge__(argument)

    def __gt__(self, argument) -> bool:
        """
        Is true when offset is greater than ``argument``.

        ..  container:: example

            With equal numerators, denominators and displacement:

            >>> offset_1 = abjad.Offset((1, 4), displacement=(-1, 16))
            >>> offset_2 = abjad.Offset((1, 4), displacement=(-1, 16))

            >>> offset_1 > offset_1
            False
            >>> offset_1 > offset_2
            False
            >>> offset_2 > offset_1
            False
            >>> offset_2 > offset_2
            False

        ..  container:: example

            With equal numerators and denominators but differing grace
            displacements:

            >>> offset_1 = abjad.Offset((1, 4), displacement=(-1, 8))
            >>> offset_2 = abjad.Offset((1, 4), displacement=(-1, 16))

            >>> offset_1 > offset_1
            False
            >>> offset_1 > offset_2
            False
            >>> offset_2 > offset_1
            True
            >>> offset_2 > offset_2
            False

        ..  container:: example

            With differing numerators and denominators. Ignores grace
            displacements:

            >>> offset_1 = abjad.Offset((1, 4))
            >>> offset_2 = abjad.Offset((1, 2), displacement=(-99))

            >>> offset_1 > offset_1
            False
            >>> offset_1 > offset_2
            False
            >>> offset_2 > offset_1
            True
            >>> offset_2 > offset_2
            False

        """
        if isinstance(argument, type(self)) and self.pair() == argument.pair():
            return self._get_displacement() > argument._get_displacement()
        return Duration.__gt__(self, argument)

    @typing.no_type_check
    def __hash__(self) -> int:
        """
        Hashes offset.
        """
        return hash((self.pair(), self._get_displacement()))

    def __le__(self, argument) -> bool:
        """
        Is true when offset is less than or equal to ``argument``.

        ..  container:: example

            With equal numerators, denominators and displacement:

            >>> offset_1 = abjad.Offset((1, 4), displacement=(-1, 16))
            >>> offset_2 = abjad.Offset((1, 4), displacement=(-1, 16))

            >>> offset_1 <= offset_1
            True
            >>> offset_1 <= offset_2
            True
            >>> offset_2 <= offset_1
            True
            >>> offset_2 <= offset_2
            True

        ..  container:: example

            With equal numerators and denominators but differing grace
            displacements:

            >>> offset_1 = abjad.Offset((1, 4), displacement=(-1, 8))
            >>> offset_2 = abjad.Offset((1, 4), displacement=(-1, 16))

            >>> offset_1 <= offset_1
            True
            >>> offset_1 <= offset_2
            True
            >>> offset_2 <= offset_1
            False
            >>> offset_2 <= offset_2
            True

        ..  container:: example

            With differing numerators and denominators. Ignores grace
            displacements:

            >>> offset_1 = abjad.Offset((1, 4))
            >>> offset_2 = abjad.Offset((1, 2), displacement=(-99))

            >>> offset_1 <= offset_1
            True
            >>> offset_1 <= offset_2
            True
            >>> offset_2 <= offset_1
            False
            >>> offset_2 <= offset_2
            True

        """
        if isinstance(argument, type(self)) and self.pair() == argument.pair():
            return self._get_displacement() <= argument._get_displacement()
        return super().__le__(argument)

    def __lt__(self, argument) -> bool:
        """
        Is true when offset is less than ``argument``.

        With equal numerators, denominators and displacement:

        ..  container:: example

            >>> offset_1 = abjad.Offset((1, 4), displacement=(-1, 16))
            >>> offset_2 = abjad.Offset((1, 4), displacement=(-1, 16))

            >>> offset_1 < offset_1
            False
            >>> offset_1 < offset_2
            False
            >>> offset_2 < offset_1
            False
            >>> offset_2 < offset_2
            False

        ..  container:: example

            With equal numerators and denominators but differing nonzero grace
            displacements:

            >>> offset_1 = abjad.Offset((1, 4), displacement=(-1, 8))
            >>> offset_2 = abjad.Offset((1, 4), displacement=(-1, 16))

            >>> offset_1 < offset_1
            False
            >>> offset_1 < offset_2
            True
            >>> offset_2 < offset_1
            False
            >>> offset_2 < offset_2
            False

        ..  container:: example

            With equal numerators and denominators but differing zero-valued
            displacement:

            >>> offset_1 = abjad.Offset((1, 4), displacement=(-1, 8))
            >>> offset_2 = abjad.Offset((1, 4))

            >>> offset_1 < offset_1
            False
            >>> offset_1 < offset_2
            True
            >>> offset_2 < offset_1
            False
            >>> offset_2 < offset_2
            False

        ..  container:: example

            With differing numerators and denominators. Ignores grace
            displacements:

            >>> offset_1 = abjad.Offset((1, 4))
            >>> offset_2 = abjad.Offset((1, 2), displacement=(-99))

            >>> offset_1 < offset_1
            False
            >>> offset_1 < offset_2
            True
            >>> offset_2 < offset_1
            False
            >>> offset_2 < offset_2
            False

        """
        if isinstance(argument, type(self)) and self.pair() == argument.pair():
            return self._get_displacement() < argument._get_displacement()
        return super().__lt__(argument)

    def __repr__(self) -> str:
        """
        Gets interpreter representation of offset.

        ..  container:: example

            >>> abjad.Offset(1, 4)
            Offset((1, 4))

            >>> abjad.Offset(1, 4, displacement=(-1, 16))
            Offset((1, 4), displacement=Duration(-1, 16))

        """
        if self.displacement() is None:
            return f"{type(self).__name__}({self.pair()})"
        else:
            string = f"{self.pair()}, displacement={self.displacement()!r}"
            return f"{type(self).__name__}({string})"

    def __sub__(self, argument):
        """
        Subtracts ``argument`` from offset.

        ..  container:: example

            Offset taken from offset returns duration:

            >>> abjad.Offset(2) - abjad.Offset(1, 2)
            Duration(3, 2)

            Duration taken from offset returns another offset:

            >>> abjad.Offset(2) - abjad.Duration(1, 2)
            Offset((3, 2))

        ..  container::

            Coerces ``argument`` to offset when ``argument`` is neither offset
            nor duration:

            >>> import fractions
            >>> abjad.Offset(2) - fractions.Fraction(1, 2)
            Duration(3, 2)

        """
        if isinstance(argument, type(self)):
            return Duration(super().__sub__(argument))
        elif isinstance(argument, Duration):
            return super().__sub__(argument)
        else:
            argument = type(self)(argument)
            return self - argument

    def _get_displacement(self):
        if self.displacement() is None:
            return Duration(0)
        return self.displacement()

    def displacement(self):
        """
        Gets displacement.

        ..  container:: example

            Gets displacement equal to none:

            >>> offset = abjad.Offset(1, 4)
            >>> offset.displacement() is None
            True

        ..  container:: example

            Gets displacement equal to a negative sixteenth:

            >>> offset = abjad.Offset(1, 4, displacement=(-1, 16))
            >>> offset.displacement()
            Duration(-1, 16)

        ..  container:: example

            Stores zero-valued displacement as none:

            >>> offset = abjad.Offset(1, 4, displacement=0)
            >>> offset.displacement() is None
            True

            >>> offset
            Offset((1, 4))

        """
        return self._displacement


@dataclasses.dataclass(frozen=True, order=True, slots=True, unsafe_hash=True)
class Ratio:
    """
    Ratio.

    Abjad ratios are two-term, unreduced integer ratios of the form ``n:d``.

    These are used primarily in modeling tuplet ratios like ``3:2`` and ``6:4``.
    """

    numerator: int
    denominator: int

    def __post_init__(self):
        assert isinstance(self.numerator, int), repr(self.numerator)
        assert isinstance(self.denominator, int), repr(self.denominator)

    def __mul__(self, n: int) -> "Ratio":
        """
        Multiplies numerator and denominator of ratio by ``n``.

        ..  container:: example

            >>> abjad.Ratio(3, 2) * 2
            Ratio(numerator=6, denominator=4)

        """
        assert isinstance(n, int), repr(n)
        return Ratio(n * self.numerator, n * self.denominator)

    def __truediv__(self, n: int) -> "Ratio":
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

    def __rmul__(self, n: int) -> "Ratio":
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

    def reciprocal(self) -> "Ratio":
        """
        Get reciprocal of ratio.

        ..  container:: example

            >>> abjad.Ratio(6, 4).reciprocal()
            Ratio(numerator=4, denominator=6)

        """
        return Ratio(self.denominator, self.numerator)


def divide_pair(pair: tuple[int, int], n: int | Duration) -> tuple[int, int]:
    """
    Divides ``pair`` by integer or duration ``n``.
    """
    assert isinstance(pair, tuple), repr(pair)
    assert isinstance(n, int | Duration), repr(n)
    fraction = fractions.Fraction(*pair) / n
    denominator = _math.least_common_multiple(pair[1], fraction.denominator)
    pair = with_denominator(fraction, denominator)
    return pair


def durations(items: list) -> list[Duration]:
    """
    Changes ``items`` to durations.

    ..  container:: example

        >>> abjad.durations([(15, 8), (3, 8)])
        [Duration(15, 8), Duration(3, 8)]

    """
    durations = [Duration(_) for _ in items]
    return durations


def fraction_from_dot_count(dot_count: int) -> fractions.Fraction:
    """
    Makes fraction from ``dot_count``.

    ..  container:: example

        >>> abjad.duration.fraction_from_dot_count(0)
        Fraction(1, 1)

        >>> abjad.duration.fraction_from_dot_count(1)
        Fraction(3, 2)

        >>> abjad.duration.fraction_from_dot_count(2)
        Fraction(7, 4)

        >>> abjad.duration.fraction_from_dot_count(3)
        Fraction(15, 8)

        >>> abjad.duration.fraction_from_dot_count(4)
        Fraction(31, 16)

    """
    assert isinstance(dot_count, int), repr(dot_count)
    assert 0 <= dot_count, repr(dot_count)
    denominator = 2**dot_count
    numerator = 2 ** (dot_count + 1) - 1
    return fractions.Fraction(numerator, denominator)


def pair(argument: typing.Any) -> tuple[int, int]:
    """
    Changes ``argument`` to pair.

    ..  container:: example

        >>> abjad.duration.pair((3, 6))
        (3, 6)

        >>> abjad.duration.pair(abjad.Fraction(3, 6))
        (1, 2)

        >>> abjad.duration.pair(abjad.Duration(3, 6))
        (1, 2)

        >>> abjad.duration.pair(abjad.Offset((3, 6)))
        (1, 2)

        >>> abjad.duration.pair(abjad.TimeSignature((3, 6)))
        (3, 6)

    """
    if hasattr(argument, "numerator"):
        return argument.numerator, argument.denominator
    if isinstance(argument, tuple) and len(argument) == 2:
        return argument[0], argument[1]
    raise ValueError(argument)


def with_denominator(duration, denominator) -> tuple[int, int]:
    """
    Spells ``duration`` as pair with ``denominator``.

    ..  container:: example

        >>> abjad.duration.with_denominator(abjad.Duration(3, 6), 12)
        (6, 12)

    ..  container:: example

        >>> for numerator in range(12):
        ...     fraction = abjad.Fraction(numerator, 6)
        ...     print(fraction, abjad.duration.with_denominator(fraction, 12))
        ...
        0 (0, 12)
        1/6 (2, 12)
        1/3 (4, 12)
        1/2 (6, 12)
        2/3 (8, 12)
        5/6 (10, 12)
        1 (12, 12)
        7/6 (14, 12)
        4/3 (16, 12)
        3/2 (18, 12)
        5/3 (20, 12)
        11/6 (22, 12)

        >>> for numerator in range(12):
        ...     pair = (numerator, 6)
        ...     print(pair, abjad.duration.with_denominator(pair, 8))
        ...
        (0, 6) (0, 8)
        (1, 6) (1, 6)
        (2, 6) (2, 6)
        (3, 6) (4, 8)
        (4, 6) (4, 6)
        (5, 6) (5, 6)
        (6, 6) (8, 8)
        (7, 6) (7, 6)
        (8, 6) (8, 6)
        (9, 6) (12, 8)
        (10, 6) (10, 6)
        (11, 6) (11, 6)

        >>> for numerator in range(12):
        ...     pair = (numerator, 6)
        ...     print(pair, abjad.duration.with_denominator(pair, 12))
        ...
        (0, 6) (0, 12)
        (1, 6) (2, 12)
        (2, 6) (4, 12)
        (3, 6) (6, 12)
        (4, 6) (8, 12)
        (5, 6) (10, 12)
        (6, 6) (12, 12)
        (7, 6) (14, 12)
        (8, 6) (16, 12)
        (9, 6) (18, 12)
        (10, 6) (20, 12)
        (11, 6) (22, 12)

    """
    if isinstance(duration, tuple):
        current_numerator, current_denominator = duration
    else:
        current_numerator, current_denominator = (
            duration.numerator,
            duration.denominator,
        )
    multiplier = fractions.Fraction(denominator, current_denominator)
    new_numerator = multiplier * current_numerator
    new_denominator = multiplier * current_denominator
    if new_numerator.denominator == 1 and new_denominator.denominator == 1:
        pair = (new_numerator.numerator, new_denominator.numerator)
    else:
        pair = (current_numerator, current_denominator)
    return pair
