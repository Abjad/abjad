# -*- encoding: utf-8 -*-
import fractions
import math
import re
from abjad.tools import mathtools
from abjad.tools.abctools import ImmutableAbjadObject


class Duration(ImmutableAbjadObject, fractions.Fraction):
    r'''Abjad model of musical duration.

    Initialize from integer numerator:

    ::

        >>> Duration(3)
        Duration(3, 1)

    Initialize from integer numerator and denominator:

    ::

        >>> Duration(3, 16)
        Duration(3, 16)

    Initialize from integer-equivalent numeric numerator:

    ::

        >>> Duration(3.0)
        Duration(3, 1)

    Initialize from integer-equivalent numeric numerator and denominator:

    ::

        >>> Duration(3.0, 16)
        Duration(3, 16)

    Initialize from integer-equivalent singleton:

    ::

        >>> Duration((3,))
        Duration(3, 1)

    Initialize from integer-equivalent pair:

    ::

        >>> Duration((3, 16))
        Duration(3, 16)

    Initialize from other duration:

    ::

        >>> Duration(Duration(3, 16))
        Duration(3, 16)

    Intialize from fraction:

    ::

        >>> Duration(Fraction(3, 16))
        Duration(3, 16)

    Initialize from solidus string:

    ::

        >>> Duration('3/16')
        Duration(3, 16)

    Initialize from nonreduced fraction:

    ::

        >>> Duration(mathtools.NonreducedFraction(3, 16))
        Duration(3, 16)

    Durations inherit from built-in fraction:

    ::

        >>> isinstance(Duration(3, 16), Fraction)
        True

    Durations are numeric:

    ::

        >>> import numbers

    ::

        >>> isinstance(Duration(3, 16), numbers.Number)
        True

    Durations are immutable.
    '''

    ### CONSTRUCTOR ###

    def __new__(cls, *args):
        from abjad.tools import sequencetools
        try:
            return fractions.Fraction.__new__(cls, *args)
        except TypeError:
            pass
        try:
            return fractions.Fraction.__new__(cls, *args[0])
        except (AttributeError, TypeError):
            pass
        try:
            return fractions.Fraction.__new__(
                cls, args[0].numerator, args[0].denominator)
        except AttributeError:
            pass
        if len(args) == 1 and \
            sequencetools.is_integer_equivalent_singleton(args[0]):
            self = fractions.Fraction.__new__(cls, int(args[0][0]))
        elif len(args) == 1 and \
            sequencetools.is_fraction_equivalent_pair(args[0]):
            self = fractions.Fraction.__new__(
                cls, int(args[0][0]), int(args[0][1]))
        elif len(args) == 1 and \
            isinstance(args[0], str) and not '/' in args[0]:
            result = Duration._init_from_lilypond_duration_string(args[0])
            self = fractions.Fraction.__new__(cls, result)
        elif sequencetools.all_are_integer_equivalent_numbers(args):
            self = fractions.Fraction.__new__(cls, *[int(x) for x in args])
        else:
            raise ValueError(args)
        return self

    ### SPECIAL METHODS ###

    def __abs__(self, *args):
        return type(self)(fractions.Fraction.__abs__(self, *args))

    def __add__(self, *args):
        if len(args) == 1 and \
            isinstance(args[0], mathtools.NonreducedFraction):
            return args[0].__radd__(self)
        else:
            return type(self)(fractions.Fraction.__add__(self, *args))

    def __div__(self, *args):
        from abjad.tools import durationtools
        if len(args) == 1 and isinstance(args[0], type(self)):
            return durationtools.Multiplier(
                fractions.Fraction.__div__(self, *args))
        elif len(args) == 1 and isinstance(
            args[0], mathtools.NonreducedFraction):
            return args[0].__rdiv__(self)
        else:
            return type(self)(fractions.Fraction.__div__(self, *args))

    def __divmod__(self, *args):
        return type(self)(fractions.Fraction.__divmod__(self, *args))

    def __eq__(self, arg):
        return fractions.Fraction.__eq__(self, arg)

    def __ge__(self, arg):
        return fractions.Fraction.__ge__(self, arg)

    def __gt__(self, arg):
        return fractions.Fraction.__gt__(self, arg)

    def __le__(self, arg):
        return fractions.Fraction.__le__(self, arg)

    def __lt__(self, arg):
        return fractions.Fraction.__lt__(self, arg)

    def __mod__(self, *args):
        return type(self)(fractions.Fraction.__mod__(self, *args))

    def __mul__(self, *args):
        if len(args) == 1 and \
            isinstance(args[0], mathtools.NonreducedFraction):
            return args[0].__rmul__(self)
        else:
            return type(self)(fractions.Fraction.__mul__(self, *args))

    def __ne__(self, arg):
        return fractions.Fraction.__ne__(self, arg)

    def __neg__(self, *args):
        return type(self)(fractions.Fraction.__neg__(self, *args))

    def __pos__(self, *args):
        return type(self)(fractions.Fraction.__pos__(self, *args))

    def __pow__(self, *args):
        return type(self)(fractions.Fraction.__pow__(self, *args))

    def __radd__(self, *args):
        return type(self)(fractions.Fraction.__radd__(self, *args))

    def __rdiv__(self, *args):
        return type(self)(fractions.Fraction.__rdiv__(self, *args))

    def __rdivmod__(self, *args):
        return type(self)(fractions.Fraction.__rdivmod__(self, *args))

    def __reduce__(self):
        return self.__class__, (self.numerator, self.denominator)

    def __reduce_ex__(self, protocol):
        return self.__class__, (self.numerator, self.denominator)

    def __repr__(self):
        return '%s(%s, %s)' % (
            self._class_name, self.numerator, self.denominator)

    def __rmod__(self, *args):
        return type(self)(fractions.Fraction.__rmod__(self, *args))

    def __rmul__(self, *args):
        return type(self)(fractions.Fraction.__rmul__(self, *args))

    def __rpow__(self, *args):
        return type(self)(fractions.Fraction.__rpow__(self, *args))

    def __rsub__(self, *args):
        return type(self)(fractions.Fraction.__rsub__(self, *args))

    def __rtruediv__(self, *args):
        return type(self)(fractions.Fraction.__rtruediv__(self, *args))

    def __sub__(self, *args):
        if len(args) == 1 and \
            isinstance(args[0], mathtools.NonreducedFraction):
            return args[0].__rsub__(self)
        else:
            return type(self)(fractions.Fraction.__sub__(self, *args))

    def __truediv__(self, *args):
        return type(self)(fractions.Fraction.__truediv__(self, *args))

    ### PRIVATE PROPERTIES ###

    @property
    def _keyword_argument_names(self):
        return ()

    @property
    def _positional_argument_values(self):
        result = []
        result.append(self.numerator)
        result.append(self.denominator)
        return tuple(result)

    ### PRIVATE METHODS ###

    # do not indent in storage
    def _get_tools_package_qualified_repr_pieces(self, is_indented=True):
        return [''.join(
            ImmutableAbjadObject._get_tools_package_qualified_repr_pieces(
                self, is_indented=False))]

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
    def _init_from_lilypond_duration_string(duration_string):
        numeric_body_strings = [str(2 ** n) for n in range(8)]
        other_body_strings = [r'\\breve', r'\\longa', r'\\maxima']
        body_strings = numeric_body_strings + other_body_strings
        body_strings = '|'.join(body_strings)
        pattern = r'^(%s)(\.*)$' % body_strings
        match = re.match(pattern, duration_string)
        if match is None:
            message = 'incorrect duration string format: {!r}.'
            raise DurationError(message.format(duration_string))
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
                raise ValueError(message.format(body_string))
        rational = body_duration
        for n in range(len(dots_string)):
            exponent = n + 1
            denominator = 2 ** exponent
            multiplier = fractions.Fraction(1, denominator)
            addend = multiplier * body_duration
            rational += addend
        return rational

    ### PUBLIC PROPERTIES ###

    @property
    def dot_count(self):
        r'''Positive integer number of dots required to notate duration:

        ::

            >>> for n in range(1, 16 + 1):
            ...     try:
            ...         duration = Duration(n, 16)
            ...         print '{}\t{}'.format(
            ...             duration.with_denominator(16), duration.dot_count)
            ...     except AssignabilityError:
            ...         print '{}\t{}'.format(
            ...             duration.with_denominator(16), '--')
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

        Return positive integer.

        Raise assignability error when duration is not assignable.
        '''
        if not self.is_assignable:
            raise AssignabilityError
        binary_string = mathtools.integer_to_binary_string(self.numerator)
        digit_sum = sum([int(x) for x in list(binary_string)])
        dot_count = digit_sum - 1
        return dot_count

    @property
    def equal_or_greater_assignable(self):
        r'''Equal or greater assignable:

        ::

            >>> for numerator in range(1, 16 + 1):
            ...     duration = Duration(numerator, 16)
            ...     result = duration.equal_or_greater_assignable
            ...     print '{}\t{}'.format(
            ...         duration.with_denominator(16), result)
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

        Return new duration.
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
        r'''Equal or greater power of ``2``:

        ::

            >>> for numerator in range(1, 16 + 1):
            ...     duration = Duration(numerator, 16)
            ...     result = duration.equal_or_greater_power_of_two
            ...     print '{}\t{}'.format(
            ...         duration.with_denominator(16), result)
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

        Return new duration.
        '''
        denominator_exponent = -int(math.ceil(math.log(self, 2)))
        return type(self)(1, 2) ** denominator_exponent

    @property
    def equal_or_lesser_assignable(self):
        r'''Equal or lesser assignable:

        ::

            >>> for numerator in range(1, 16 + 1):
            ...     duration = Duration(numerator, 16)
            ...     result = duration.equal_or_lesser_assignable
            ...     print '{}\t{}'.format(
            ...         duration.with_denominator(16), result)
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

        Return new duration.
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
        r'''Equal or lesser power of ``2``:

        ::

            >>> for numerator in range(1, 16 + 1):
            ...     duration = Duration(numerator, 16)
            ...     result = duration.equal_or_lesser_power_of_two
            ...     print '{}\t{}'.format(
            ...         duration.with_denominator(16), result)
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

        Return new duration.
        '''
        denominator_exponent = -int(math.floor(math.log(self, 2)))
        return type(self)(1, 2) ** denominator_exponent

    @property
    def flag_count(self):
        r'''Nonnegative integer number of flags required to notate duration:

        ::

            >>> for n in range(1, 16 + 1):
            ...     duration = Duration(n, 64)
            ...     print '{}\t{}'.format(
            ...         duration.with_denominator(64), duration.flag_count)
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

        Return nonnegative integer.
        '''
        # TODO: rewrite with only one operation per line
        flag_count = max(-int(math.floor(math.log(float(self.numerator) /
            self.denominator, 2))) - 2, 0)
        return flag_count

    @property
    def has_power_of_two_denominator(self):
        r'''True when duration is an integer power of ``2``.
        Otherwise false:

        ::

            >>> for n in range(1, 16 + 1):
            ...     duration = Duration(1, n)
            ...     print '{}\t{}'.format(duration, 
            ...         duration.has_power_of_two_denominator)
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

        Return boolean.
        '''
        exponent = math.log(self.denominator, 2)
        return int(exponent) == exponent

    @property
    def implied_prolation(self):
        r'''Implied prolation of multiplier:

        ::

            >>> for denominator in range(1, 16 + 1):
            ...     multiplier = Multiplier(1, denominator)
            ...     print '{}\t{}'.format(multiplier, 
            ...         multiplier.implied_prolation)
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

        Return new multipler.
        '''
        from abjad.tools import durationtools
        numerator = \
            mathtools.greatest_power_of_two_less_equal(self.denominator)
        return durationtools.Multiplier(numerator, self.denominator)

    @property
    def is_assignable(self):
        r'''True when assignable. Otherwise false:

        ::

            >>> for numerator in range(0, 16 + 1):
            ...     duration = Duration(numerator, 16)
            ...     print '{}\t{}'.format(duration.with_denominator(16), 
            ...         duration.is_assignable)
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

        Return boolean.
        '''
        if 0 < self < 16:
            if mathtools.is_nonnegative_integer_power_of_two(
                self.denominator):
                if mathtools.is_assignable_integer(self.numerator):
                    return True
        return False

    @property
    def lilypond_duration_string(self):
        r'''LilyPond duration string of assignable duration.

            >>> Duration(3, 16).lilypond_duration_string
            '8.'

        Return string.

        Raise assignability error when duration is not assignable.
        '''
        from abjad.tools import durationtools

        if not self.is_assignable:
            raise AssignabilityError
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
        '''Pair of duration numerator and denominator:

        ::

            >>> duration = Duration(3, 16)

        ::

            >>> duration.pair
            (3, 16)

        Return integer pair.
        '''
        return self.numerator, self.denominator

    @property
    def prolation_string(self):
        r'''Prolation string:

        ::

            >>> generator = Duration.yield_durations(unique=True)
            >>> for n in range(16):
            ...     rational = generator.next()
            ...     duration = Duration(rational)
            ...     print '{}\t{}'.format(duration, duration.prolation_string)
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

        Return string.
        '''
        return '{}:{}'.format(self.denominator, self.numerator)

    @property
    def reciprocal(self):
        '''Reciprocal of duration.

        Return newly constructed duration.
        '''
        return type(self)(self.denominator, self.numerator)

    ### PUBLIC FUNCTIONS ###

    @staticmethod
    def durations_to_nonreduced_fractions_with_common_denominator(durations):
        r'''Change `durations` to nonreduced fractions with 
        least common denominator:

        ::

            >>> durations = [Duration(2, 4), 3, (5, 16)]
            >>> for x in Duration.durations_to_nonreduced_fractions_with_common_denominator(
            ...     durations):
            ...     x
            ...
            NonreducedFraction(8, 16)
            NonreducedFraction(48, 16)
            NonreducedFraction(5, 16)

        Return new object of `durations` type.
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
        r'''Initialize from LilyPond duration string:

        ::

            >>> Duration.from_lilypond_duration_string('8.')
            Duration(3, 16)

        Return duration.
        '''
        fraction = Duration._init_from_lilypond_duration_string(
            lilypond_duration_string)
        return Duration(fraction)

    @staticmethod
    def is_token(expr):
        '''True if `expr` correctly initializes a duration.
        Otherwise false.

            >>> Duration.is_token('8.')
            True

        Return boolean.
        '''
        try:
            Duration.__new__(Duration, expr)
            return True
        except:
            return False

    def to_clock_string(self, escape_ticks=False):
        r'''Change duration to clock string.

        ..  container:: example

            **Example 1.** Change numeric `seconds` to clock string:

            ::

                >>> duration = Duration(117)
                >>> duration.to_clock_string()
                '1\'57"'

        ..  container:: example

            **Example 2.** Change numeric `seconds` to escaped clock string:

            ::

                >>> note = Note("c'4")
                >>> clock_string = duration.to_clock_string(escape_ticks=True)

            ::

                >>> markuptools.Markup('"%s"' % clock_string, Up)(note)
                Markup(('1\'57\\"',), direction=Up)(c'4)

            ..  doctest::

                >>> f(note)
                c'4 ^ \markup { 1'57\\" }

        Return string.
        '''
        if self < 0:
            raise ValueError('seconds must be positive.')
        minutes = int(self / 60)
        remaining_seconds = str(int(self - minutes * 60)).zfill(2)
        if escape_ticks:
            clock_string = "%s'%s\\\"" % (minutes, remaining_seconds)
        else:
            clock_string = "%s'%s\"" % (minutes, remaining_seconds)
        return clock_string

    def with_denominator(self, denominator):
        r'''Duration with `denominator`:

        ::

            >>> duration = Duration(1, 4)

        ::

            >>> for denominator in (4, 8, 16, 32):
            ...     print duration.with_denominator(denominator)
            ...
            1/4
            2/8
            4/16
            8/32

        Return new duration.
        '''
        nonreduced_fraction = mathtools.NonreducedFraction(self)
        return nonreduced_fraction.with_denominator(denominator)

    @staticmethod
    def yield_durations(unique=False):
        r'''Yield durations.

        ..  container:: example

            **Example 1.** Yield all positive durations in 
            Cantor diagonalized order:

            ::

                >>> generator = Duration.yield_durations()
                >>> for n in range(16):
                ...     generator.next()
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

            **Example 2.** Yield all positive durations in 
            Cantor diagonalized order uniquely:

            ::

                >>> generator = Duration.yield_durations(unique=True)
                >>> for n in range(16):
                ...     generator.next()
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

        Return generator.
        '''
        generator = mathtools.yield_nonreduced_fractions()
        while True:
            integer_pair = generator.next()
            duration = Duration(integer_pair)
            if not unique:
                yield duration
            elif duration.pair == integer_pair:
                yield duration
