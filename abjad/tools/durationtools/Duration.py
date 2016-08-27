# -*- coding: utf-8 -*-
import copy
import fractions
import math
import re
from abjad.tools import mathtools
from abjad.tools import systemtools
from abjad.tools.abctools.AbjadObject import AbjadObject
from abjad.tools.topleveltools.override import override
from abjad.tools.topleveltools.set_ import set_


class Duration(AbjadObject, fractions.Fraction):
    r'''Duration.

    ..  container:: example

        **Example 1.** Initializes from integer numerator:

        ::

            >>> Duration(3)
            Duration(3, 1)

    ..  container:: example

        **Example 2.** Initializes from integer numerator and denominator:

        ::

            >>> Duration(3, 16)
            Duration(3, 16)

    ..  container:: example

        **Example 3.** Initializes from integer-equivalent numeric numerator:

        ::

            >>> Duration(3.0)
            Duration(3, 1)

    ..  container:: example

        **Example 4.** Initializes from integer-equivalent numeric numerator
        and denominator:

        ::

            >>> Duration(3.0, 16)
            Duration(3, 16)

    ..  container:: example

        **Example 5.** Initializes from integer-equivalent singleton:

        ::

            >>> Duration((3,))
            Duration(3, 1)

    ..  container:: example

        **Example 6.** Initializes from integer-equivalent pair:

        ::

            >>> Duration((3, 16))
            Duration(3, 16)

    ..  container:: example

        **Example 7.** Initializes from other duration:

        ::

            >>> Duration(Duration(3, 16))
            Duration(3, 16)

    ..  container:: example

        **Example 8.** Intializes from fraction:

        ::

            >>> Duration(Fraction(3, 16))
            Duration(3, 16)

    ..  container:: example

        **Example 9.** Initializes from solidus string:

        ::

            >>> Duration('3/16')
            Duration(3, 16)

    ..  container:: example

        **Example 10.** Initializes from nonreduced fraction:

        ::

            >>> Duration(mathtools.NonreducedFraction(6, 32))
            Duration(3, 16)

    ..  container:: example

        **Example 11.** Durations inherit from built-in fraction:

        ::

            >>> isinstance(Duration(3, 16), Fraction)
            True

    ..  container:: example

        **Example 12.** Durations are numeric:

        ::

            >>> import numbers

        ::

            >>> isinstance(Duration(3, 16), numbers.Number)
            True

    '''

    ### CLASS VARIABLES ###

    __slots__ = (
        )

    ### CONSTRUCTOR ###

    def __new__(class_, *args):
        if len(args) == 1:
            arg = args[0]
            if type(arg) is class_:
                return arg
            if isinstance(arg, mathtools.NonreducedFraction):
                return fractions.Fraction.__new__(class_, *arg.pair)
            try:
                return fractions.Fraction.__new__(class_, *arg)
            except (AttributeError, TypeError):
                pass
            try:
                return fractions.Fraction.__new__(class_, arg)
            except (AttributeError, TypeError):
                pass
            if mathtools.is_fraction_equivalent_pair(arg):
                return fractions.Fraction.__new__(
                    class_, int(arg[0]), int(arg[1]))
            if hasattr(arg, 'duration'):
                return fractions.Fraction.__new__(class_, arg.duration)
            if isinstance(arg, str) and '/' not in arg:
                result = Duration._initialize_from_lilypond_duration_string(
                    arg)
                return fractions.Fraction.__new__(class_, result)
            if mathtools.is_integer_equivalent_singleton(arg):
                return fractions.Fraction.__new__(class_, int(arg[0]))
        else:
            try:
                return fractions.Fraction.__new__(class_, *args)
            except TypeError:
                pass
            if mathtools.all_are_integer_equivalent_numbers(args):
                return fractions.Fraction.__new__(
                    class_,
                    *[int(x) for x in args]
                    )
        message = 'can not construct duration: {!r}.'
        message = message.format(args)
        raise ValueError(message)

    ### SPECIAL METHODS ###

    def __abs__(self, *args):
        r'''Gets absolute value of duration.

        Returns nonnegative duration.
        '''
        return type(self)(fractions.Fraction.__abs__(self, *args))

    def __add__(self, *args):
        r'''Adds duration to `args`.

        ..  container:: example

            **Example 1.** Returns duration when `args` is a duration:

            ::

                >>> duration_1 = Duration(1, 2)
                >>> duration_2 = Duration(3, 2)
                >>> duration_1 + duration_2
                Duration(2, 1)

        ..  container:: example

            **Example 2.** Returns nonreduced fraction when `args` is a
            nonreduced fraction:

            ::

                >>> duration = Duration(1, 2)
                >>> nonreduced_fraction = mathtools.NonreducedFraction(3, 6)
                >>> duration + nonreduced_fraction
                NonreducedFraction(6, 6)

        Returns duration.
        '''
        if (
            len(args) == 1 and
            isinstance(args[0], mathtools.NonreducedFraction)
            ):
            result = args[0].__radd__(self)
        else:
            result = type(self)(fractions.Fraction.__add__(self, *args))
        return result

    def __div__(self, *args):
        r'''Divides duration by `args`.

        Returns multiplier.
        '''
        from abjad.tools import durationtools
        if len(args) == 1 and isinstance(args[0], type(self)):
            fraction = fractions.Fraction.__truediv__(self, *args)
            result = durationtools.Multiplier(fraction)
        elif len(args) == 1 and isinstance(
            args[0], mathtools.NonreducedFraction):
            result = args[0].__rdiv__(self)
        else:
            result = type(self)(fractions.Fraction.__truediv__(self, *args))
        return result

    def __divmod__(self, *args):
        r'''Equals the pair (duration // `args`, duration % `args`).

        Returns pair.
        '''
        truncated, residue = fractions.Fraction.__divmod__(self, *args)
        truncated = type(self)(truncated)
        residue = type(self)(residue)
        return truncated, residue

    def __eq__(self, arg):
        r'''Is true when duration equals `arg`.
        Otherwise false.

        Returns true or false.
        '''
        return fractions.Fraction.__eq__(self, arg)

    def __format__(self, format_specification=''):
        r'''Formats duration.

        Set `format_specification` to `''` or `'storage'`.
        Interprets `''` equal to `'storage'`.

        Returns string.
        '''
        from abjad.tools import systemtools
        if format_specification in ('', 'storage'):
            return systemtools.StorageFormatAgent(self).get_storage_format()
        return str(self)

    def __ge__(self, arg):
        r'''Is true when duration is greater than or equal to `arg`.
        Otherwise false.

        Returns true or false.
        '''
        return fractions.Fraction.__ge__(self, arg)

    def __gt__(self, arg):
        r'''Is true when duration is greater than `arg`.
        Otherwise false.

        Returns true or false.
        '''
        return fractions.Fraction.__gt__(self, arg)

    def __hash__(self):
        r'''Hashes duration.

        Required to be explicitly redefined on Python 3 if __eq__ changes.

        Returns integer.
        '''
        return super(Duration, self).__hash__()

    def __le__(self, arg):
        r'''Is true when duration is less than or equal to `arg`.
        Otherwise false.

        Returns true or false.
        '''
        return fractions.Fraction.__le__(self, arg)

    def __lt__(self, arg):
        r'''Is true when duration is less than `arg`.
        Otherwise false.

        Returns true or false.
        '''
        return fractions.Fraction.__lt__(self, arg)

    def __mod__(self, *args):
        r'''Modulus operator applied to duration.

        Returns duration.
        '''
        return type(self)(fractions.Fraction.__mod__(self, *args))

    def __mul__(self, *args):
        r'''Duration multiplied by `args`.

        ..  container:: example

            **Example 1.** Returns a new duration when `args` is a duration:

            ::

                >>> duration_1 = Duration(1, 2)
                >>> duration_2 = Duration(3, 2)
                >>> duration_1 * duration_2
                Duration(3, 4)

        ..  container:: example

            **Example 2.** Returns nonreduced fraction when `args` is a
            nonreduced fraction:

            ::

                >>> duration = Duration(1, 2)
                >>> nonreduced_fraction = mathtools.NonreducedFraction(3, 6)
                >>> duration * nonreduced_fraction
                NonreducedFraction(3, 12)

        Returns duration or nonreduced fraction.
        '''
        if (
            len(args) == 1 and
            isinstance(args[0], mathtools.NonreducedFraction)
            ):
            result = args[0].__rmul__(self)
        else:
            result = type(self)(fractions.Fraction.__mul__(self, *args))
        return result

    def __ne__(self, arg):
        r'''Is true when duration does not equal `arg`.
        Otherwise false.

        Returns true or false.
        '''
        return fractions.Fraction.__ne__(self, arg)

    def __neg__(self, *args):
        r'''Negates duration.

        Returns new duration.
        '''
        return type(self)(fractions.Fraction.__neg__(self, *args))

    def __pos__(self, *args):
        r'''Get positive duration.

        Returns new duration.
        '''
        return type(self)(fractions.Fraction.__pos__(self, *args))

    def __pow__(self, *args):
        r'''Raises duration to `args` power.

        Returns new duration.
        '''
        return type(self)(fractions.Fraction.__pow__(self, *args))

    def __radd__(self, *args):
        r'''Adds `args` to duration.

        Returns new duration.
        '''
        return type(self)(fractions.Fraction.__radd__(self, *args))

    def __rdiv__(self, *args):
        r'''Divides `args` by duration.

        Returns new duration.
        '''
        return type(self)(fractions.Fraction.__rdiv__(self, *args))

    def __rdivmod__(self, *args):
        r'''Documentation required.
        '''
        return type(self)(fractions.Fraction.__rdivmod__(self, *args))

    def __reduce__(self):
        r'''Documentation required.
        '''
        return type(self), (self.numerator, self.denominator)

    def __reduce_ex__(self, protocol):
        r'''Documentation required.
        '''
        return type(self), (self.numerator, self.denominator)

    def __rmod__(self, *args):
        r'''Documentation required.
        '''
        return type(self)(fractions.Fraction.__rmod__(self, *args))

    def __rmul__(self, *args):
        r'''Multiplies `args` by duration.

        Returns new duration.
        '''
        return type(self)(fractions.Fraction.__rmul__(self, *args))

    def __rpow__(self, *args):
        r'''Raises `args` to the power of duration.

        Returns new duration.
        '''
        return type(self)(fractions.Fraction.__rpow__(self, *args))

    def __rsub__(self, *args):
        r'''Subtracts duration from `args`.

        Returns new duration.
        '''
        return type(self)(fractions.Fraction.__rsub__(self, *args))

    def __rtruediv__(self, *args):
        r'''Documentation required.

        Returns new duration.
        '''
        return type(self)(fractions.Fraction.__rtruediv__(self, *args))

    def __sub__(self, *args):
        r'''Subtracts `args` from duration.

        Returns new duration.
        '''
        if (
            len(args) == 1 and
            isinstance(args[0], mathtools.NonreducedFraction)
            ):
            return args[0].__rsub__(self)
        else:
            return type(self)(fractions.Fraction.__sub__(self, *args))

    def __truediv__(self, *args):
        r'''Documentation required.
        '''
        return self.__div__(*args)

    ### PRIVATE METHODS ###

    def _get_format_specification(self):
        return systemtools.FormatSpecification(
            client=self,
            storage_format_args_values=[
                self.numerator,
                self.denominator,
                ],
            storage_format_is_indented=False,
            storage_format_kwargs_names=[],
            )

    @staticmethod
    def _group_nonreduced_fractions_by_implied_prolation(durations):
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
            body_duration = fractions.Fraction(1, body_denominator)
        except ValueError:
            if body_string == r'\breve':
                body_duration = fractions.Fraction(2)
            elif body_string == r'\longa':
                body_duration = fractions.Fraction(4)
            elif body_string == r'\maxima':
                body_duration = fractions.Fraction(8)
            else:
                message = 'unknown body string: {!r}.'
                message = message.format(body_string)
                raise ValueError(message)
        rational = body_duration
        for n in range(len(dots_string)):
            exponent = n + 1
            denominator = 2 ** exponent
            multiplier = fractions.Fraction(1, denominator)
            addend = multiplier * body_duration
            rational += addend
        return rational

    @staticmethod
    def _make_markup_score_block(selection):
        from abjad.tools import lilypondfiletools
        from abjad.tools import schemetools
        from abjad.tools import scoretools
        selection = copy.deepcopy(selection)
        staff = scoretools.Staff(selection)
        staff.context_name = 'RhythmicStaff'
        staff.remove_commands.append('Time_signature_engraver')
        staff.remove_commands.append('Staff_symbol_engraver')
        override(staff).stem.direction = Up
        #override(staff).stem.length = 4
        override(staff).stem.length = 5
        override(staff).tuplet_bracket.bracket_visibility = True
        override(staff).tuplet_bracket.direction = Up
        override(staff).tuplet_bracket.padding = 1.25
        override(staff).tuplet_bracket.shorten_pair = (-1, -1.5)
        scheme = schemetools.Scheme('tuplet-number::calc-fraction-text')
        override(staff).tuplet_number.text = scheme
        set_(staff).tuplet_full_length = True
        layout_block = lilypondfiletools.Block(name='layout')
        layout_block.indent = 0
        layout_block.ragged_right = True
        score = scoretools.Score([staff])
        override(score).spacing_spanner.spacing_increment = 0.5
        set_(score).proportional_notation_duration = False
        return score, layout_block

    @staticmethod
    def _to_score_markup(selection):
        from abjad.tools import markuptools
        staff, layout_block = Duration._make_markup_score_block(selection)
        command = markuptools.MarkupCommand('score', [staff, layout_block])
        markup = markuptools.Markup(command)
        return markup

    ### PUBLIC PROPERTIES ###

    @property
    def dot_count(self):
        r'''Gets dot count.

        ..  container:: example

            **Example.** Gets dot count:

            ::

                >>> for n in range(1, 16 + 1):
                ...     try:
                ...         duration = Duration(n, 16)
                ...         sixteenths = duration.with_denominator(16)
                ...         dot_count = duration.dot_count
                ...         string = '{!s}\t{}'
                ...         string = string.format(sixteenths, dot_count)
                ...         print(string)
                ...     except AssignabilityError:
                ...         sixteenths = duration.with_denominator(16)
                ...         string = '{!s}\t{}'
                ...         string = string.format(sixteenths, '--')
                ...         print(string)
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
        '''
        if not self.is_assignable:
            raise AssignabilityError
        binary_string = mathtools.integer_to_binary_string(self.numerator)
        digit_sum = sum([int(x) for x in list(binary_string)])
        dot_count = digit_sum - 1
        return dot_count

    @property
    def equal_or_greater_assignable(self):
        r'''Gets assignable duration equal to or just greater than this
        duration.

        ..  container:: example

            **Example.** Gets equal-or-greater assignable duration:

            ::

                >>> for numerator in range(1, 16 + 1):
                ...     duration = Duration(numerator, 16)
                ...     result = duration.equal_or_greater_assignable
                ...     sixteenths = duration.with_denominator(16)
                ...     print('{!s}\t{!s}'.format(sixteenths, result))
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
        '''
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
        r'''Gets duration equal or just greater power of two.

        ..  container:: example

            **Example.** Gets equal-or-greater power-of-two:

            ::

                >>> for numerator in range(1, 16 + 1):
                ...     duration = Duration(numerator, 16)
                ...     result = duration.equal_or_greater_power_of_two
                ...     sixteenths = duration.with_denominator(16)
                ...     print('{!s}\t{!s}'.format(sixteenths, result))
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
        '''
        denominator_exponent = -int(math.ceil(math.log(self, 2)))
        return type(self)(1, 2) ** denominator_exponent

    @property
    def equal_or_lesser_assignable(self):
        r'''Gets assignable duration equal or just less than this duration.

        ..  container:: example

            **Example.** Gets equal-or-lesser assignable duration:

            ::

                >>> for numerator in range(1, 16 + 1):
                ...     duration = Duration(numerator, 16)
                ...     result = duration.equal_or_lesser_assignable
                ...     sixteenths = duration.with_denominator(16)
                ...     print('{!s}\t{!s}'.format(sixteenths, result))
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
        '''
        good_denominator = mathtools.least_power_of_two_greater_equal(
            self.denominator)
        current_numerator = self.numerator
        candidate = type(self)(current_numerator, good_denominator)
        while not candidate.is_assignable:
            current_numerator -= 1
            candidate = type(self)(current_numerator, good_denominator)
        return candidate

    @property
    def equal_or_lesser_power_of_two(self):
        r'''Gets duration of the form ``d**2`` equal to or just less than this
        duration.

        ..  container:: example

            **Example.** Gets equal-or-lesser power-of-two:

            ::

                >>> for numerator in range(1, 16 + 1):
                ...     duration = Duration(numerator, 16)
                ...     result = duration.equal_or_lesser_power_of_two
                ...     sixteenths = duration.with_denominator(16)
                ...     print('{!s}\t{!s}'.format(sixteenths, result))
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
        '''
        denominator_exponent = -int(math.floor(math.log(self, 2)))
        return type(self)(1, 2) ** denominator_exponent

    @property
    def flag_count(self):
        r'''Gets flag count.

        ..  container:: example

            **Example.** Gets flag count:

            ::

                >>> for n in range(1, 16 + 1):
                ...     duration = Duration(n, 64)
                ...     sixty_fourths = duration.with_denominator(64)
                ...     print('{!s}\t{}'.format(sixty_fourths, duration.flag_count))
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
        '''
        # TODO: rewrite with only one operation per line
        flag_count = max(-int(math.floor(math.log(float(self.numerator) /
            self.denominator, 2))) - 2, 0)
        return flag_count

    @property
    def has_power_of_two_denominator(self):
        r'''Is true when duration is an integer power of two.
        Otherwise false.

        ..  container:: example

            **Example.** Is true when duration has power-of-two denominator:

            ::

                >>> for n in range(1, 16 + 1):
                ...     duration = Duration(1, n)
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
        '''
        exponent = math.log(self.denominator, 2)
        return int(exponent) == exponent

    @property
    def implied_prolation(self):
        r'''Gets implied prolation.

        ..  container:: example

            **Example.** Gets implied prolation:

            ::

                >>> for denominator in range(1, 16 + 1):
                ...     duration = Duration(1, denominator)
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
        '''
        from abjad.tools import durationtools
        numerator = \
            mathtools.greatest_power_of_two_less_equal(self.denominator)
        return durationtools.Multiplier(numerator, self.denominator)

    @property
    def is_assignable(self):
        r'''Is true when duration is assignable. Otherwise false.

        ..  container:: example

            **Example.** Is true when duration is assignable:

            ::

                >>> for numerator in range(0, 16 + 1):
                ...     duration = Duration(numerator, 16)
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
        '''
        if 0 < self < 16:
            if mathtools.is_nonnegative_integer_power_of_two(
                self.denominator):
                if mathtools.is_assignable_integer(self.numerator):
                    return True
        return False

    @property
    def lilypond_duration_string(self):
        r'''Gets LilyPond duration string.

        ..  container:: example

            **Example.** Gets LilyPond duration string:

                >>> Duration(3, 16).lilypond_duration_string
                '8.'

        Raises assignability error when duration is not assignable.

        Returns string.
        '''
        if not self.is_assignable:
            raise AssignabilityError(self)
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
        '''Gets numerator and denominator.

        ..  container:: example

            **Example.** Gets pair:

            ::

                >>> Duration(3, 16).pair
                (3, 16)

        Returns integer pair.
        '''
        return self.numerator, self.denominator

    @property
    def prolation_string(self):
        r'''Gets prolation string.

        ..  container:: example

            **Example.** Gets prolation string:

            ::

                >>> generator = Duration.yield_durations(unique=True)
                >>> for n in range(16):
                ...     duration = next(generator)
                ...     string = '{!s}\t{}'
                ...     string = string.format(duration, duration.prolation_string)
                ...     print(string)
                ...
                1       1:1
                2       1:2
                1/2     2:1
                1/3     3:1
                3       1:3
                4       1:4
                3/2     2:3
                2/3     3:2
                1/4     4:1
                1/5     5:1
                5       1:5
                6       1:6
                5/2     2:5
                4/3     3:4
                3/4     4:3
                2/5     5:2

        Returns string.
        '''
        return '{}:{}'.format(self.denominator, self.numerator)

    @property
    def reciprocal(self):
        '''Gets reciprocal.

        ..  container:: example

            **Example.** Gets reciprocal:

            ::

                >>> Duration(3, 7).reciprocal
                Duration(7, 3)

        Returns new duration.
        '''
        return type(self)(self.denominator, self.numerator)

    ### PUBLIC FUNCTIONS ###

    @staticmethod
    def durations_to_nonreduced_fractions(durations):
        r'''Changes `durations` to nonreduced fractions sharing
        least common denominator.

        ..  container:: example

            **Example.** Changes durations to nonreduced fractions:

            ::

                >>> durations = [Duration(2, 4), 3, (5, 16)]
                >>> result = Duration.durations_to_nonreduced_fractions(durations)
                >>> for x in result:
                ...     x
                ...
                NonreducedFraction(8, 16)
                NonreducedFraction(48, 16)
                NonreducedFraction(5, 16)

        Returns new object of `durations` type.
        '''
        durations = [Duration(x) for x in durations]
        denominators = [duration.denominator for duration in durations]
        lcd = mathtools.least_common_multiple(*denominators)
        nonreduced_fractions = [
            mathtools.NonreducedFraction(x).with_denominator(lcd)
            for x in durations
            ]
        result = type(durations)(nonreduced_fractions)
        return result

    @staticmethod
    def from_lilypond_duration_string(lilypond_duration_string):
        r'''Initializes duration from LilyPond duration string.

        ..  container:: example

            **Example.** Initializes duration from LilyPond duration string:

            ::

                >>> Duration.from_lilypond_duration_string('8.')
                Duration(3, 16)

        Returns duration.
        '''
        fraction = Duration._initialize_from_lilypond_duration_string(
            lilypond_duration_string)
        return Duration(fraction)

    @staticmethod
    def is_token(expr):
        '''Is true when `expr` correctly initializes a duration.
        Otherwise false.

        ..  container:: example

            **Example.** Is true when expression is a duration token:

            ::

                >>> Duration.is_token('8.')
                True

        Returns true or false.
        '''
        try:
            Duration.__new__(Duration, expr)
            return True
        except:
            return False

    def to_clock_string(self):
        r'''Changes duration to clock string.

        ..  container:: example

            **Example.** Changes duration to clock string:

            ::

                >>> note = Note("c'4")
                >>> duration = Duration(117)
                >>> clock_string = duration.to_clock_string()
                >>> clock_string
                "1'57''"

            ::

                >>> string = '"{}"'.format(clock_string)
                >>> markup = markuptools.Markup(string, direction=Up)
                >>> attach(markup, note)
                >>> show(note) # doctest: +SKIP

            ..  doctest::

                >>> print(format(note))
                c'4 ^ \markup { 1'57'' }

        Rounds down to nearest second.

        Returns string.
        '''
        minutes = int(self / 60)
        seconds = str(int(self - minutes * 60)).zfill(2)
        clock_string = "{}'{}''".format(minutes, seconds)
        return clock_string

    def to_score_markup(self):
        r'''Changes duration to score markup.

        ..  container:: example

            **Example 1.** Changes assignable duration to score markup:

            ::

                >>> markup = Duration(3, 16).to_score_markup()
                >>> show(markup) # doctest: +SKIP

            ..  doctest::

                >>> f(markup)
                \markup {
                    \score
                        {
                            \new Score \with {
                                \override SpacingSpanner.spacing-increment = #0.5
                                proportionalNotationDuration = ##f
                            } <<
                                \new RhythmicStaff \with {
                                    \remove Time_signature_engraver
                                    \remove Staff_symbol_engraver
                                    \override Stem.direction = #up
                                    \override Stem.length = #5
                                    \override TupletBracket.bracket-visibility = ##t
                                    \override TupletBracket.direction = #up
                                    \override TupletBracket.padding = #1.25
                                    \override TupletBracket.shorten-pair = #'(-1 . -1.5)
                                    \override TupletNumber.text = #tuplet-number::calc-fraction-text
                                    tupletFullLength = ##t
                                } {
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

            **Example 2.** Changes nonassignable duration to score markup:

            ::

                >>> markup = Duration(5, 16).to_score_markup()
                >>> show(markup) # doctest: +SKIP

            ..  doctest::

                >>> f(markup)
                \markup {
                    \score
                        {
                            \new Score \with {
                                \override SpacingSpanner.spacing-increment = #0.5
                                proportionalNotationDuration = ##f
                            } <<
                                \new RhythmicStaff \with {
                                    \remove Time_signature_engraver
                                    \remove Staff_symbol_engraver
                                    \override Stem.direction = #up
                                    \override Stem.length = #5
                                    \override TupletBracket.bracket-visibility = ##t
                                    \override TupletBracket.direction = #up
                                    \override TupletBracket.padding = #1.25
                                    \override TupletBracket.shorten-pair = #'(-1 . -1.5)
                                    \override TupletNumber.text = #tuplet-number::calc-fraction-text
                                    tupletFullLength = ##t
                                } {
                                    c'4 ~
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

            **Example 3.** Override tuplet number text like this:

            ::

                >>> tuplet = Tuplet((5, 7), "c'16 c' c' c' c' c' c'")
                >>> attach(Beam(), tuplet[:])
                >>> staff = Staff([tuplet], context_name='RhythmicStaff')
                >>> duration = inspect_(tuplet).get_duration()
                >>> markup = duration.to_score_markup()
                >>> markup = markup.scale((0.75, 0.75))
                >>> override(tuplet).tuplet_number.text = markup
                >>> show(staff) # doctest: +SKIP

            ..  doctest::

                >>> f(staff)
                \new RhythmicStaff {
                    \override TupletNumber.text = \markup {
                        \scale
                            #'(0.75 . 0.75)
                            \score
                                {
                                    \new Score \with {
                                        \override SpacingSpanner.spacing-increment = #0.5
                                        proportionalNotationDuration = ##f
                                    } <<
                                        \new RhythmicStaff \with {
                                            \remove Time_signature_engraver
                                            \remove Staff_symbol_engraver
                                            \override Stem.direction = #up
                                            \override Stem.length = #5
                                            \override TupletBracket.bracket-visibility = ##t
                                            \override TupletBracket.direction = #up
                                            \override TupletBracket.padding = #1.25
                                            \override TupletBracket.shorten-pair = #'(-1 . -1.5)
                                            \override TupletNumber.text = #tuplet-number::calc-fraction-text
                                            tupletFullLength = ##t
                                        } {
                                            c'4 ~
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
                        c'16 [
                        c'16
                        c'16
                        c'16
                        c'16
                        c'16
                        c'16 ]
                    }
                    \revert TupletNumber.text
                }

        Returns markup.
        '''
        from abjad.tools import scoretools
        notes = scoretools.make_leaves([0], [self])
        markup = self._to_score_markup(notes)
        return markup

    def with_denominator(self, denominator):
        r'''Changes duration to nonreduced fraction with `denominator`.

        ..  container:: example

            **Example.** Changes duration to nonreduced fraction:

            ::

                >>> duration = Duration(1, 4)
                >>> for denominator in (4, 8, 16, 32):
                ...     print(duration.with_denominator(denominator))
                ...
                1/4
                2/8
                4/16
                8/32

        Returns new duration.
        '''
        nonreduced_fraction = mathtools.NonreducedFraction(self)
        return nonreduced_fraction.with_denominator(denominator)

    @staticmethod
    def yield_durations(unique=False):
        r'''Yields all positive durations.

        ..  container:: example

            **Example 1.** Yields all positive durations in Cantor diagonalized
            order:

            ::

                >>> generator = Duration.yield_durations()
                >>> for n in range(16):
                ...     next(generator)
                ...
                Duration(1, 1)
                Duration(2, 1)
                Duration(1, 2)
                Duration(1, 3)
                Duration(1, 1)
                Duration(3, 1)
                Duration(4, 1)
                Duration(3, 2)
                Duration(2, 3)
                Duration(1, 4)
                Duration(1, 5)
                Duration(1, 2)
                Duration(1, 1)
                Duration(2, 1)
                Duration(5, 1)
                Duration(6, 1)

        ..  container:: example

            **Example 2.** Yields all positive durations in Cantor diagonalized
            order uniquely:

            ::

                >>> generator = Duration.yield_durations(unique=True)
                >>> for n in range(16):
                ...     next(generator)
                ...
                Duration(1, 1)
                Duration(2, 1)
                Duration(1, 2)
                Duration(1, 3)
                Duration(3, 1)
                Duration(4, 1)
                Duration(3, 2)
                Duration(2, 3)
                Duration(1, 4)
                Duration(1, 5)
                Duration(5, 1)
                Duration(6, 1)
                Duration(5, 2)
                Duration(4, 3)
                Duration(3, 4)
                Duration(2, 5)

        Returns generator.
        '''
        generator = mathtools.yield_nonreduced_fractions()
        while True:
            integer_pair = next(generator)
            duration = Duration(integer_pair)
            if not unique:
                yield duration
            elif duration.pair == integer_pair:
                yield duration

    def yield_equivalent_durations(self, minimum_written_duration=None):
        r'''Yields all durations equivalent to this duration.

        Returns output in Cantor diagonalized order.

        Ensures written duration never less than `minimum_written_duration`.

        ..  container:: example

            **Example 1.** Yields durations equivalent to ``1/8``:

            ::

                >>> pairs = Duration(1, 8).yield_equivalent_durations()
                >>> for pair in pairs: pair
                ...
                (Multiplier(1, 1), Duration(1, 8))
                (Multiplier(2, 3), Duration(3, 16))
                (Multiplier(4, 3), Duration(3, 32))
                (Multiplier(4, 7), Duration(7, 32))
                (Multiplier(8, 7), Duration(7, 64))
                (Multiplier(8, 15), Duration(15, 64))
                (Multiplier(16, 15), Duration(15, 128))
                (Multiplier(16, 31), Duration(31, 128))

        ..  container:: example

            **Example 2.** Yields durations equivalent ot ``1/12``:

            ::

                >>> pairs = Duration(1, 12).yield_equivalent_durations()
                >>> for pair in pairs: pair
                ...
                (Multiplier(2, 3), Duration(1, 8))
                (Multiplier(4, 3), Duration(1, 16))
                (Multiplier(8, 9), Duration(3, 32))
                (Multiplier(16, 9), Duration(3, 64))
                (Multiplier(16, 21), Duration(7, 64))
                (Multiplier(32, 21), Duration(7, 128))
                (Multiplier(32, 45), Duration(15, 128))

        ..  container:: example

            Yields durations equivalent to ``5/48``:

            ::

                >>> pairs = Duration(5, 48).yield_equivalent_durations()
                >>> for pair in pairs: pair
                ...
                (Multiplier(5, 6), Duration(1, 8))
                (Multiplier(5, 3), Duration(1, 16))
                (Multiplier(5, 9), Duration(3, 16))
                (Multiplier(10, 9), Duration(3, 32))
                (Multiplier(20, 21), Duration(7, 64))
                (Multiplier(40, 21), Duration(7, 128))
                (Multiplier(8, 9), Duration(15, 128))

        Defaults `minimum_written_duration` to ``1/128``.

        Returns generator.
        '''
        if minimum_written_duration is None:
            minimum_written_duration = type(self)(1, 128)
        else:
            minimum_written_duration = type(self)(minimum_written_duration)
        generator = type(self).yield_durations(unique=True)
        pairs = []
        while True:
            written_duration = next(generator)
            if not written_duration.is_assignable:
                continue
            if written_duration < minimum_written_duration:
                pairs = tuple(pairs)
                return pairs
            prolation = self / written_duration
            if prolation.is_proper_tuplet_multiplier:
                pair = (prolation, written_duration)
                pairs.append(pair)
