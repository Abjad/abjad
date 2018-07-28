import copy
import math
import re
import typing
from abjad import exceptions
from abjad import mathtools
from abjad.system.AbjadObject import AbjadObject
try:
    from quicktions import Fraction  # type: ignore
except ImportError:
    from fractions import Fraction


class Duration(AbjadObject, Fraction):
    """
    Duration.

    ..  container:: example

        Initializes from integer numerator:

        >>> abjad.Duration(3)
        Duration(3, 1)

    ..  container:: example

        Initializes from integer numerator and denominator:

        >>> abjad.Duration(3, 16)
        Duration(3, 16)

    ..  container:: example

        Initializes from integer-equivalent numeric numerator:

        >>> abjad.Duration(3.0)
        Duration(3, 1)

    ..  container:: example

        Initializes from integer-equivalent numeric numerator and denominator:

        >>> abjad.Duration(3.0, 16)
        Duration(3, 16)

    ..  container:: example

        Initializes from integer-equivalent singleton:

        >>> abjad.Duration((3,))
        Duration(3, 1)

    ..  container:: example

        Initializes from integer-equivalent pair:

        >>> abjad.Duration((3, 16))
        Duration(3, 16)

    ..  container:: example

        Initializes from other duration:

        >>> abjad.Duration(abjad.Duration(3, 16))
        Duration(3, 16)

    ..  container:: example

        Intializes from fraction:

        >>> abjad.Duration(abjad.Fraction(3, 16))
        Duration(3, 16)

    ..  container:: example

        Initializes from solidus string:

        >>> abjad.Duration('3/16')
        Duration(3, 16)

    ..  container:: example

        Initializes from nonreduced fraction:

        >>> abjad.Duration(abjad.NonreducedFraction(6, 32))
        Duration(3, 16)

    ..  container:: example

        Durations inherit from built-in fraction:

        >>> isinstance(abjad.Duration(3, 16), abjad.Fraction)
        True

    ..  container:: example

        Durations are numbers:

        >>> import numbers

        >>> isinstance(abjad.Duration(3, 16), numbers.Number)
        True

    """

    ### CLASS VARIABLES ###

    __slots__ = ()

    ### CONSTRUCTOR ###

    def __new__(class_, *arguments):
        if len(arguments) == 1:
            argument = arguments[0]
            if type(argument) is class_:
                return argument
            if isinstance(argument, mathtools.NonreducedFraction):
                return Fraction.__new__(class_, *argument.pair)
            try:
                return Fraction.__new__(class_, *argument)
            except (AttributeError, TypeError):
                pass
            try:
                return Fraction.__new__(class_, argument)
            except (AttributeError, TypeError):
                pass
            if (isinstance(argument, tuple) and
                len(argument) == 2 and
                mathtools.is_integer_equivalent(argument[0]) and
                mathtools.is_integer_equivalent(argument[1]) and
                not argument[1] == 0):
                return Fraction.__new__(
                    class_,
                    int(argument[0]),
                    int(argument[1]),
                    )
            try:
                return Fraction.__new__(class_, argument.duration)
            except AttributeError:
                pass
            if isinstance(argument, str) and '/' not in argument:
                result = Duration._initialize_from_lilypond_duration_string(
                    argument)
                return Fraction.__new__(class_, result)
            if (isinstance(argument, tuple) and
                len(argument) == 1 and
                mathtools.is_integer_equivalent(argument[0])):
                return Fraction.__new__(class_, int(argument[0]))
        else:
            try:
                return Fraction.__new__(class_, *arguments)
            except TypeError:
                pass
            if mathtools.all_are_integer_equivalent_numbers(arguments):
                return Fraction.__new__(
                    class_,
                    *[int(x) for x in arguments]
                    )
        message = 'can not construct duration: {!r}.'
        message = message.format(arguments)
        raise ValueError(message)

    ### SPECIAL METHODS ###

    def __abs__(self, *arguments):
        """
        Gets absolute value of duration.

        Returns nonnegative duration.
        """
        return type(self)(Fraction.__abs__(self, *arguments))

    def __add__(self, *arguments):
        """
        Adds duration to ``arguments``.

        ..  container:: example

            Returns duration when ``arguments`` is a duration:

            >>> duration_1 = abjad.Duration(1, 2)
            >>> duration_2 = abjad.Duration(3, 2)
            >>> duration_1 + duration_2
            Duration(2, 1)

        ..  container:: example

            Returns nonreduced fraction when ``arguments`` is a nonreduced
            fraction:

            >>> duration = abjad.Duration(1, 2)
            >>> nonreduced_fraction = abjad.NonreducedFraction(3, 6)
            >>> duration + nonreduced_fraction
            NonreducedFraction(6, 6)

        Returns duration.
        """
        if (
            len(arguments) == 1 and
            isinstance(arguments[0], mathtools.NonreducedFraction)
            ):
            result = arguments[0].__radd__(self)
        else:
            result = type(self)(Fraction.__add__(self, *arguments))
        return result

    def __div__(self, *arguments):
        """
        Divides duration by ``arguments``.

        ..  container:: example

            >>> abjad.Duration(1) / abjad.NonreducedFraction(3, 3)
            NonreducedFraction(3, 3)


        >>> abjad.NonreducedFraction(3, 3) / abjad.Duration(1)
        NonreducedFraction(3, 3)

        Returns multiplier.
        """
        import abjad
        if len(arguments) == 1 and isinstance(arguments[0], type(self)):
            fraction = Fraction.__truediv__(self, *arguments)
            result = abjad.Multiplier(fraction)
        elif len(arguments) == 1 and isinstance(
            arguments[0], abjad.NonreducedFraction):
            result = arguments[0].__rdiv__(self)
        else:
            result = type(self)(Fraction.__truediv__(self, *arguments))
        return result

    def __divmod__(self, *arguments):
        """
        Equals the pair (duration // ``arguments``, duration % ``arguments``).

        Returns pair.
        """
        truncated, residue = Fraction.__divmod__(self, *arguments)
        truncated = type(self)(truncated)
        residue = type(self)(residue)
        return truncated, residue

    def __eq__(self, argument):
        """
        Is true when duration equals ``argument``.

        Returns true or false.
        """
        return Fraction.__eq__(self, argument)

    def __format__(self, format_specification=''):
        """
        Formats duration.

        Set ``format_specification`` to ``''`` or ``'storage'``.
        Interprets ``''`` equal to ``'storage'``.

        Returns string.
        """
        import abjad
        if format_specification in ('', 'storage'):
            return abjad.StorageFormatManager(self).get_storage_format()
        return str(self)

    def __ge__(self, argument):
        """
        Is true when duration is greater than or equal to ``argument``.

        Returns true or false.
        """
        return Fraction.__ge__(self, argument)

    def __gt__(self, argument):
        """
        Is true when duration is greater than ``argument``.

        Returns true or false.
        """
        return Fraction.__gt__(self, argument)

    def __hash__(self):
        """
        Hashes duration.

        Required to be explicitly redefined on Python 3 if __eq__ changes.

        Returns integer.
        """
        return super().__hash__()

    def __le__(self, argument):
        """
        Is true when duration is less than or equal to ``argument``.

        Returns true or false.
        """
        return Fraction.__le__(self, argument)

    def __lt__(self, argument):
        """
        Is true when duration is less than ``argument``.

        Returns true or false.
        """
        return Fraction.__lt__(self, argument)

    def __mod__(self, *arguments):
        """
        Modulus operator applied to duration.

        Returns duration.
        """
        return type(self)(Fraction.__mod__(self, *arguments))

    def __mul__(self, *arguments):
        """
        Duration multiplied by ``arguments``.

        ..  container:: example

            Returns a new duration when ``arguments`` is a duration:

            >>> duration_1 = abjad.Duration(1, 2)
            >>> duration_2 = abjad.Duration(3, 2)
            >>> duration_1 * duration_2
            Duration(3, 4)

        ..  container:: example

            Returns nonreduced fraction when ``arguments`` is a nonreduced
            fraction:

            >>> duration = abjad.Duration(1, 2)
            >>> nonreduced_fraction = abjad.NonreducedFraction(3, 6)
            >>> duration * nonreduced_fraction
            NonreducedFraction(3, 12)

        Returns duration or nonreduced fraction.
        """
        if (
            len(arguments) == 1 and
            isinstance(arguments[0], mathtools.NonreducedFraction)
            ):
            result = arguments[0].__rmul__(self)
        else:
            result = type(self)(Fraction.__mul__(self, *arguments))
        return result

    def __neg__(self, *arguments):
        """
        Negates duration.

        Returns new duration.
        """
        return type(self)(Fraction.__neg__(self, *arguments))

    def __pos__(self, *arguments):
        """
        Get positive duration.

        Returns new duration.
        """
        return type(self)(Fraction.__pos__(self, *arguments))

    def __pow__(self, *arguments):
        """
        Raises duration to ``arguments`` power.

        Returns new duration.
        """
        return type(self)(Fraction.__pow__(self, *arguments))

    def __radd__(self, *arguments):
        """
        Adds ``arguments`` to duration.

        Returns new duration.
        """
        return type(self)(Fraction.__radd__(self, *arguments))

    def __rdiv__(self, *arguments):
        """
        Divides ``arguments`` by duration.

        Returns new duration.
        """
        return type(self)(Fraction.__rdiv__(self, *arguments))

    def __rdivmod__(self, *arguments):
        """
        Documentation required.
        """
        return type(self)(Fraction.__rdivmod__(self, *arguments))

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

    def __rmod__(self, *arguments):
        """
        Documentation required.
        """
        return type(self)(Fraction.__rmod__(self, *arguments))

    def __rmul__(self, *arguments):
        """
        Multiplies ``arguments`` by duration.

        Returns new duration.
        """
        return type(self)(Fraction.__rmul__(self, *arguments))

    def __rpow__(self, *arguments):
        """
        Raises ``arguments`` to the power of duration.

        Returns new duration.
        """
        return type(self)(Fraction.__rpow__(self, *arguments))

    def __rsub__(self, *arguments):
        """
        Subtracts duration from ``arguments``.

        Returns new duration.
        """
        return type(self)(Fraction.__rsub__(self, *arguments))

    def __rtruediv__(self, *arguments):
        """
        Documentation required.

        Returns new duration.
        """
        return type(self)(Fraction.__rtruediv__(self, *arguments))

    def __sub__(self, *arguments):
        """
        Subtracts ``arguments`` from duration.

        ..  container:: example

            >>> abjad.Duration(1, 2) - abjad.NonreducedFraction(2, 8)
            NonreducedFraction(2, 8)

            >>> abjad.NonreducedFraction(4, 8) - abjad.Duration(1, 4)
            NonreducedFraction(2, 8)

        Returns new duration.
        """
        if (
            len(arguments) == 1 and
            isinstance(arguments[0], mathtools.NonreducedFraction)
            ):
            return arguments[0].__rsub__(self)
        else:
            return type(self)(Fraction.__sub__(self, *arguments))

    def __truediv__(self, *arguments):
        """
        Documentation required.
        """
        return self.__div__(*arguments)

    ### PRIVATE METHODS ###

    def _get_format_specification(self):
        import abjad
        return abjad.FormatSpecification(
            client=self,
            storage_format_args_values=[
                self.numerator,
                self.denominator,
                ],
            storage_format_is_indented=False,
            storage_format_kwargs_names=[],
            )

    @staticmethod
    def _group_by_implied_prolation(durations):
        durations = [
            mathtools.NonreducedFraction(duration)
            for duration in durations
            ]
        assert 0 < len(durations)
        group = [durations[0]]
        result = [group]
        for d in durations[1:]:
            d_f = set(mathtools.factors(d.denominator))
            d_f.discard(2)
            gd_f = set(mathtools.factors(group[0].denominator))
            gd_f.discard(2)
            if d_f == gd_f:
                group.append(d)
            else:
                group = [d]
                result.append(group)
        return result

    @staticmethod
    def _initialize_from_lilypond_duration_string(duration_string):
        numeric_body_strings = [str(2 ** n) for n in range(8)]
        other_body_strings = [r'\\breve', r'\\longa', r'\\maxima']
        body_strings = numeric_body_strings + other_body_strings
        body_strings = '|'.join(body_strings)
        pattern = r'^(%s)(\.*)$' % body_strings
        match = re.match(pattern, duration_string)
        if match is None:
            message = 'incorrect duration string format: {!r}.'
            message = message.format(duration_string)
            raise TypeError(message)
        body_string, dots_string = match.groups()
        try:
            body_denominator = int(body_string)
            body_duration = Fraction(1, body_denominator)
        except ValueError:
            if body_string == r'\breve':
                body_duration = Fraction(2)
            elif body_string == r'\longa':
                body_duration = Fraction(4)
            elif body_string == r'\maxima':
                body_duration = Fraction(8)
            else:
                message = 'unknown body string: {!r}.'
                message = message.format(body_string)
                raise ValueError(message)
        rational = body_duration
        for n in range(len(dots_string)):
            exponent = n + 1
            denominator = 2 ** exponent
            multiplier = Fraction(1, denominator)
            addend = multiplier * body_duration
            rational += addend
        return rational

    @staticmethod
    def _least_power_of_two_greater_equal(n, i=0):
        """
        When ``i = 2``, returns the second integer power of 2 greater than
        the least integer power of 2 greater than or equal to ``n``, and, in
        general, return the ``i`` th integer power of 2 greater than the least
        integer power of 2 greater than or equal to ``n``.

        Returns integer.
        """
        assert isinstance(n, (int, float, Fraction)), repr(n)
        assert 0 <= n, repr(n)
        result = 2 ** (int(math.ceil(math.log(n, 2))) + i)
        return result

    @staticmethod
    def _make_markup_score_block(selection):
        import abjad
        selection = copy.deepcopy(selection)
        staff = abjad.Staff(selection)
        staff.lilypond_type = 'RhythmicStaff'
        staff.remove_commands.append('Time_signature_engraver')
        staff.remove_commands.append('Staff_symbol_engraver')
        abjad.override(staff).stem.direction = abjad.Up
        abjad.override(staff).stem.length = 5
        abjad.override(staff).tuplet_bracket.bracket_visibility = True
        abjad.override(staff).tuplet_bracket.direction = abjad.Up
        abjad.override(staff).tuplet_bracket.minimum_length = 4
        abjad.override(staff).tuplet_bracket.padding = 1.25
        abjad.override(staff).tuplet_bracket.shorten_pair = (-1, -1.5)
        scheme = abjad.Scheme('ly:spanner::set-spacing-rods')
        abjad.override(staff).tuplet_bracket.springs_and_rods = scheme
        abjad.override(staff).tuplet_number.font_size = 0
        scheme = abjad.Scheme('tuplet-number::calc-fraction-text')
        abjad.override(staff).tuplet_number.text = scheme
        abjad.setting(staff).tuplet_full_length = True
        layout_block = abjad.Block(name='layout')
        layout_block.indent = 0
        layout_block.ragged_right = True
        score = abjad.Score([staff])
        abjad.override(score).spacing_spanner.spacing_increment = 0.5
        abjad.setting(score).proportional_notation_duration = False
        return score, layout_block

    @staticmethod
    def _to_score_markup(selection):
        import abjad
        staff, layout_block = Duration._make_markup_score_block(selection)
        command = abjad.MarkupCommand('score', [staff, layout_block])
        markup = abjad.Markup(command)
        return markup

    ### PUBLIC PROPERTIES ###

    @property
    def dot_count(self):
        r"""
        Gets dot count.

        ..  container:: example

            Gets dot count:

            >>> for n in range(1, 16 + 1):
            ...     try:
            ...         duration = abjad.Duration(n, 16)
            ...         sixteenths = duration.with_denominator(16)
            ...         dot_count = duration.dot_count
            ...         string = f'{sixteenths!s}\t{dot_count}'
            ...         print(string)
            ...     except abjad.AssignabilityError:
            ...         sixteenths = duration.with_denominator(16)
            ...         print(f'{sixteenths!s}\t--')
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

        Dot count defined equal to number of dots required to notate duration.

        Raises assignability error when duration is not assignable.

        Returns positive integer.
        """
        if not self.is_assignable:
            raise exceptions.AssignabilityError
        binary_string = mathtools.integer_to_binary_string(self.numerator)
        digit_sum = sum([int(x) for x in list(binary_string)])
        dot_count = digit_sum - 1
        return dot_count

    @property
    def equal_or_greater_assignable(self):
        r"""
        Gets assignable duration equal to or just greater than this
        duration.

        ..  container:: example

            Gets equal-or-greater assignable duration:

            >>> for numerator in range(1, 16 + 1):
            ...     duration = abjad.Duration(numerator, 16)
            ...     result = duration.equal_or_greater_assignable
            ...     sixteenths = duration.with_denominator(16)
            ...     print(f'{sixteenths!s}\t{result!s}')
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

        Returns new duration.
        """
        good_denominator = mathtools.greatest_power_of_two_less_equal(
            self.denominator)
        current_numerator = self.numerator
        candidate = type(self)(current_numerator, good_denominator)
        while not candidate.is_assignable:
            current_numerator += 1
            candidate = type(self)(current_numerator, good_denominator)
        return candidate

    @property
    def equal_or_greater_power_of_two(self):
        r"""
        Gets duration equal or just greater power of two.

        ..  container:: example

            Gets equal-or-greater power-of-two:

            >>> for numerator in range(1, 16 + 1):
            ...     duration = abjad.Duration(numerator, 16)
            ...     result = duration.equal_or_greater_power_of_two
            ...     sixteenths = duration.with_denominator(16)
            ...     print(f'{sixteenths!s}\t{result!s}')
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

        Returns new duration.
        """
        denominator_exponent = -int(math.ceil(math.log(self, 2)))
        return type(self)(1, 2) ** denominator_exponent

    @property
    def equal_or_lesser_assignable(self):
        r"""
        Gets assignable duration equal or just less than this duration.

        ..  container:: example

            Gets equal-or-lesser assignable duration:

            >>> for numerator in range(1, 16 + 1):
            ...     duration = abjad.Duration(numerator, 16)
            ...     result = duration.equal_or_lesser_assignable
            ...     sixteenths = duration.with_denominator(16)
            ...     print(f'{sixteenths!s}\t{result!s}')
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

        Returns new duration.
        """
        good_denominator = self._least_power_of_two_greater_equal(
            self.denominator)
        current_numerator = self.numerator
        candidate = type(self)(current_numerator, good_denominator)
        while not candidate.is_assignable:
            current_numerator -= 1
            candidate = type(self)(current_numerator, good_denominator)
        return candidate

    @property
    def equal_or_lesser_power_of_two(self):
        r"""
        Gets duration of the form ``d**2`` equal to or just less than this
        duration.

        ..  container:: example

            Gets equal-or-lesser power-of-two:

            >>> for numerator in range(1, 16 + 1):
            ...     duration = abjad.Duration(numerator, 16)
            ...     result = duration.equal_or_lesser_power_of_two
            ...     sixteenths = duration.with_denominator(16)
            ...     print(f'{sixteenths!s}\t{result!s}')
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

        Returns new duration.
        """
        denominator_exponent = -int(math.floor(math.log(self, 2)))
        return type(self)(1, 2) ** denominator_exponent

    @property
    def flag_count(self):
        r"""
        Gets flag count.

        ..  container:: example

            Gets flag count:

            >>> for n in range(1, 16 + 1):
            ...     duration = abjad.Duration(n, 64)
            ...     sixty_fourths = duration.with_denominator(64)
            ...     print(f'{sixty_fourths!s}\t{duration.flag_count}')
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

        Flag count defined equal to number of flags required to notate
        duration.

        Returns nonnegative integer.
        """
        log = math.log(float(self.numerator) / self.denominator, 2)
        count = -int(math.floor(log)) - 2
        return max(count, 0)

    @property
    def has_power_of_two_denominator(self):
        r"""
        Is true when duration is an integer power of two.

        ..  container:: example

            Is true when duration has power-of-two denominator:

            >>> for n in range(1, 16 + 1):
            ...     duration = abjad.Duration(1, n)
            ...     result = duration.has_power_of_two_denominator
            ...     print('{!s}\t{}'.format(duration, result))
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

        Returns true or false.
        """
        exponent = math.log(self.denominator, 2)
        return int(exponent) == exponent

    @property
    def implied_prolation(self):
        r"""
        Gets implied prolation.

        ..  container:: example

            Gets implied prolation:

            >>> for denominator in range(1, 16 + 1):
            ...     duration = abjad.Duration(1, denominator)
            ...     result = duration.implied_prolation
            ...     print('{!s}\t{!s}'.format(duration, result))
            ...
            1       1
            1/2     1
            1/3     2/3
            1/4     1
            1/5     4/5
            1/6     2/3
            1/7     4/7
            1/8     1
            1/9     8/9
            1/10    4/5
            1/11    8/11
            1/12    2/3
            1/13    8/13
            1/14    4/7
            1/15    8/15
            1/16    1

        Returns multipler.
        """
        import abjad
        numerator = \
            mathtools.greatest_power_of_two_less_equal(self.denominator)
        return abjad.Multiplier(numerator, self.denominator)

    @property
    def is_assignable(self):
        r"""
        Is true when duration is assignable.

        ..  container:: example

            Is true when duration is assignable:

            >>> for numerator in range(0, 16 + 1):
            ...     duration = abjad.Duration(numerator, 16)
            ...     sixteenths = duration.with_denominator(16)
            ...     print('{!s}\t{}'.format(sixteenths, duration.is_assignable))
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

        Returns true or false.
        """
        if 0 < self < 16:
            if mathtools.is_nonnegative_integer_power_of_two(
                self.denominator):
                if mathtools.is_assignable_integer(self.numerator):
                    return True
        return False

    @property
    def lilypond_duration_string(self):
        """
        Gets LilyPond duration string.

        ..  container:: example

            Gets LilyPond duration string:

                >>> abjad.Duration(3, 16).lilypond_duration_string
                '8.'

        Raises assignability error when duration is not assignable.

        Returns string.
        """
        if not self.is_assignable:
            raise exceptions.AssignabilityError(self)
        undotted_rational = self.equal_or_lesser_power_of_two
        if undotted_rational <= 1:
            undotted_duration_string = str(undotted_rational.denominator)
        elif undotted_rational == type(self)(2, 1):
            undotted_duration_string = r'\breve'
        elif undotted_rational == type(self)(4, 1):
            undotted_duration_string = r'\longa'
        elif undotted_rational == type(self)(8, 1):
            undotted_duration_string = r'\maxima'
        else:
            message = 'can not process undotted rational: {}'
            message = message.format(undotted_rational)
            raise ValueError(message)
        dot_count = self.dot_count
        dot_string = '.' * dot_count
        dotted_duration_string = undotted_duration_string + dot_string
        return dotted_duration_string

    @property
    def pair(self):
        """
        Gets numerator and denominator.

        ..  container:: example

            Gets pair:

            >>> abjad.Duration(3, 16).pair
            (3, 16)

        Returns integer pair.
        """
        return self.numerator, self.denominator

    @property
    def prolation_string(self):
        """
        Gets prolation string.

        ..  container:: example

            Gets prolation string:

            >>> abjad.Duration(3, 16).prolation_string
            '16:3'

        Returns string.
        """
        return f'{self.denominator}:{self.numerator}'

    @property
    def reciprocal(self):
        """
        Gets reciprocal.

        ..  container:: example

            Gets reciprocal:

            >>> abjad.Duration(3, 7).reciprocal
            Duration(7, 3)

        Returns new duration.
        """
        return type(self)(self.denominator, self.numerator)

    ### PUBLIC FUNCTIONS ###

    @staticmethod
    def durations_to_nonreduced_fractions(
        durations: typing.List,
        ) -> typing.List[mathtools.NonreducedFraction]:
        """
        Changes ``durations`` to nonreduced fractions sharing least common
        denominator.

        ..  container:: example

            Changes durations to nonreduced fractions:

            >>> durations = [abjad.Duration(2, 4), 3, (5, 16)]
            >>> result = abjad.Duration.durations_to_nonreduced_fractions(durations)
            >>> for x in result:
            ...     x
            ...
            NonreducedFraction(8, 16)
            NonreducedFraction(48, 16)
            NonreducedFraction(5, 16)

        """
        durations_ = [Duration(_) for _ in durations]
        denominators = [_.denominator for _ in durations_]
        lcd = mathtools.least_common_multiple(*denominators)
        nonreduced_fractions = [
            mathtools.NonreducedFraction(_).with_denominator(lcd)
            for _ in durations_
            ]
        return nonreduced_fractions

    @staticmethod
    def from_lilypond_duration_string(lilypond_duration_string):
        r"""
        Initializes duration from LilyPond duration string.

        ..  container:: example

            Initializes duration from LilyPond duration string:

            >>> abjad.Duration.from_lilypond_duration_string('8.')
            Duration(3, 16)

        Returns duration.
        """
        fraction = Duration._initialize_from_lilypond_duration_string(
            lilypond_duration_string)
        return Duration(fraction)

    @staticmethod
    def is_token(argument):
        """
        Is true when ``argument`` correctly initializes a duration.

        ..  container:: example

            Is true when expression is a duration token:

            >>> abjad.Duration.is_token('8.')
            True

        Returns true or false.
        """
        try:
            Duration.__new__(Duration, argument)
            return True
        except:
            return False

    def to_clock_string(self):
        r"""
        Changes duration to clock string.

        ..  container:: example

            Changes duration to clock string:

            >>> note = abjad.Note("c'4")
            >>> duration = abjad.Duration(117)
            >>> clock_string = duration.to_clock_string()
            >>> clock_string
            "1'57''"

            >>> string = '"{}"'.format(clock_string)
            >>> markup = abjad.Markup(string, direction=abjad.Up)
            >>> abjad.attach(markup, note)
            >>> abjad.show(note) # doctest: +SKIP

            ..  docs::

                >>> abjad.f(note)
                c'4
                ^ \markup { 1'57'' }

        Rounds down to nearest second.

        Returns string.
        """
        minutes = int(self / 60)
        seconds = str(int(self - minutes * 60)).zfill(2)
        clock_string = f"{minutes}'{seconds}''"
        return clock_string

    def to_score_markup(self):
        r"""
        Changes duration to score markup.

        ..  container:: example

            Changes assignable duration to score markup:

            >>> markup = abjad.Duration(3, 16).to_score_markup()
            >>> abjad.show(markup) # doctest: +SKIP

            ..  docs::

                >>> abjad.f(markup)
                \markup {
                    \score
                        {
                            \new Score
                            \with
                            {
                                \override SpacingSpanner.spacing-increment = #0.5
                                proportionalNotationDuration = ##f
                            }
                            <<
                                \new RhythmicStaff
                                \with
                                {
                                    \remove Time_signature_engraver
                                    \remove Staff_symbol_engraver
                                    \override Stem.direction = #up
                                    \override Stem.length = #5
                                    \override TupletBracket.bracket-visibility = ##t
                                    \override TupletBracket.direction = #up
                                    \override TupletBracket.minimum-length = #4
                                    \override TupletBracket.padding = #1.25
                                    \override TupletBracket.shorten-pair = #'(-1 . -1.5)
                                    \override TupletBracket.springs-and-rods = #ly:spanner::set-spacing-rods
                                    \override TupletNumber.font-size = #0
                                    \override TupletNumber.text = #tuplet-number::calc-fraction-text
                                    tupletFullLength = ##t
                                }
                                {
                                    c'8.
                                }
                            >>
                            \layout {
                                indent = #0
                                ragged-right = ##t
                            }
                        }
                    }

        ..  container:: example

            Changes nonassignable duration to score markup:

            >>> markup = abjad.Duration(5, 16).to_score_markup()
            >>> abjad.show(markup) # doctest: +SKIP

            ..  docs::

                >>> abjad.f(markup)
                \markup {
                    \score
                        {
                            \new Score
                            \with
                            {
                                \override SpacingSpanner.spacing-increment = #0.5
                                proportionalNotationDuration = ##f
                            }
                            <<
                                \new RhythmicStaff
                                \with
                                {
                                    \remove Time_signature_engraver
                                    \remove Staff_symbol_engraver
                                    \override Stem.direction = #up
                                    \override Stem.length = #5
                                    \override TupletBracket.bracket-visibility = ##t
                                    \override TupletBracket.direction = #up
                                    \override TupletBracket.minimum-length = #4
                                    \override TupletBracket.padding = #1.25
                                    \override TupletBracket.shorten-pair = #'(-1 . -1.5)
                                    \override TupletBracket.springs-and-rods = #ly:spanner::set-spacing-rods
                                    \override TupletNumber.font-size = #0
                                    \override TupletNumber.text = #tuplet-number::calc-fraction-text
                                    tupletFullLength = ##t
                                }
                                {
                                    c'4
                                    ~
                                    c'16
                                }
                            >>
                            \layout {
                                indent = #0
                                ragged-right = ##t
                            }
                        }
                    }

        ..  container:: example

            Override tuplet number text like this:

            >>> tuplet = abjad.Tuplet((5, 7), "c'16 c' c' c' c' c' c'")
            >>> abjad.attach(abjad.Beam(), tuplet[:])
            >>> staff = abjad.Staff([tuplet], lilypond_type='RhythmicStaff')
            >>> duration = abjad.inspect(tuplet).duration()
            >>> markup = duration.to_score_markup()
            >>> markup = markup.scale((0.75, 0.75))
            >>> abjad.override(tuplet).tuplet_number.text = markup
            >>> abjad.show(staff) # doctest: +SKIP

            ..  docs::

                >>> abjad.f(staff)
                \new RhythmicStaff
                {
                    \override TupletNumber.text = \markup {
                        \scale
                            #'(0.75 . 0.75)
                            \score
                                {
                                    \new Score
                                    \with
                                    {
                                        \override SpacingSpanner.spacing-increment = #0.5
                                        proportionalNotationDuration = ##f
                                    }
                                    <<
                                        \new RhythmicStaff
                                        \with
                                        {
                                            \remove Time_signature_engraver
                                            \remove Staff_symbol_engraver
                                            \override Stem.direction = #up
                                            \override Stem.length = #5
                                            \override TupletBracket.bracket-visibility = ##t
                                            \override TupletBracket.direction = #up
                                            \override TupletBracket.minimum-length = #4
                                            \override TupletBracket.padding = #1.25
                                            \override TupletBracket.shorten-pair = #'(-1 . -1.5)
                                            \override TupletBracket.springs-and-rods = #ly:spanner::set-spacing-rods
                                            \override TupletNumber.font-size = #0
                                            \override TupletNumber.text = #tuplet-number::calc-fraction-text
                                            tupletFullLength = ##t
                                        }
                                        {
                                            c'4
                                            ~
                                            c'16
                                        }
                                    >>
                                    \layout {
                                        indent = #0
                                        ragged-right = ##t
                                    }
                                }
                        }
                    \times 5/7 {
                        c'16
                        [
                        c'16
                        c'16
                        c'16
                        c'16
                        c'16
                        c'16
                        ]
                    }
                    \revert TupletNumber.text
                }

        Returns markup.
        """
        import abjad
        maker = abjad.LeafMaker()
        notes = maker([0], [self])
        markup = self._to_score_markup(notes)
        return markup

    def with_denominator(self, denominator):
        """
        Changes duration to nonreduced fraction with ``denominator``.

        ..  container:: example

            Changes duration to nonreduced fraction:

            >>> duration = abjad.Duration(1, 4)
            >>> for denominator in (4, 8, 16, 32):
            ...     print(duration.with_denominator(denominator))
            ...
            1/4
            2/8
            4/16
            8/32

        Returns new duration.
        """
        nonreduced_fraction = mathtools.NonreducedFraction(self)
        return nonreduced_fraction.with_denominator(denominator)
