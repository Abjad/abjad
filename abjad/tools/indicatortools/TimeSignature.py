# -*- coding: utf-8 -*-
from abjad.tools import durationtools
from abjad.tools import mathtools
from abjad.tools import systemtools
from abjad.tools.abctools.AbjadValueObject import AbjadValueObject


class TimeSignature(AbjadValueObject):
    r'''Time signature.

    ..  container:: example

        **Example 1.** First time signature:

        ::

            >>> staff = Staff("c'8 d'8 e'8")
            >>> time_signature = TimeSignature((3, 8))
            >>> attach(time_signature, staff[0])
            >>> show(staff) # doctest: +SKIP

        ..  doctest::

            >>> print(format(staff))
            \new Staff {
                \time 3/8
                c'8
                d'8
                e'8
            }

    ..  container:: example

        **Example 2.** Second time signature:

        ::

            >>> staff = Staff("c'4 d'4 e'4 f'4")
            >>> time_signature = TimeSignature((4, 4))
            >>> attach(time_signature, staff[0])
            >>> show(staff) # doctest: +SKIP

        ..  doctest::

            >>> print(format(staff))
            \new Staff {
                \time 4/4
                c'4
                d'4
                e'4
                f'4
            }

    ..  container:: example

        **Example 3.** Scoped to the score context:

        ::

            >>> staff = Staff("c'8 d'8 e'8 c'8 d'8 e'8")
            >>> time_signature = TimeSignature((3, 8))
            >>> attach(time_signature, staff[0], scope=Score)

        Formats behind comments when no score is present:

        ::

            >>> print(format(staff))
            \new Staff {
                %%% \time 3/8 %%%
                c'8
                d'8
                e'8
                c'8
                d'8
                e'8
            }

            LilyPond defaults to common time.

        ::

            >>> show(staff) # doctest: +SKIP

        Formats normally when score is present:

        ::

            >>> score = Score([staff])
            >>> print(format(score))
            \new Score <<
                \new Staff {
                    \time 3/8
                    c'8
                    d'8
                    e'8
                    c'8
                    d'8
                    e'8
                }
            >>

        ::

            >>> show(score) # doctest: +SKIP

    '''

    ### CLASS VARIABLES ###

    __slots__ = (
        '_default_scope',
        '_denominator',
        '_has_non_power_of_two_denominator',
        '_multiplier',
        '_numerator',
        '_partial',
        '_partial_repr_string',
        '_suppress',
        )

    _format_slot = 'opening'

    ### INITIALIZER ###

    def __init__(self, pair=(4, 4), partial=None, suppress=None):
        from abjad.tools import scoretools
        self._default_scope = scoretools.Staff
        pair = getattr(pair, 'pair', pair)
        assert isinstance(pair, tuple), repr(pair)
        assert len(pair) == 2, repr(pair)
        numerator, denominator = pair
        assert isinstance(numerator, int), repr(numerator)
        assert isinstance(denominator, int), repr(denominator)
        self._numerator = numerator
        self._denominator = denominator
        prototype = (durationtools.Duration, type(None))
        assert isinstance(partial, prototype), repr(partial)
        self._partial = partial
        if partial is not None:
            self._partial_repr_string = ', partial=%r' % self._partial
        else:
            self._partial_repr_string = ''
        assert isinstance(suppress, (bool, type(None))), repr(suppress)
        self._suppress = suppress
        self._multiplier = self.implied_prolation
        self._has_non_power_of_two_denominator = \
            not mathtools.is_nonnegative_integer_power_of_two(
                self.denominator)

    ### SPECIAL METHODS ###

    def __add__(self, arg):
        r'''Adds time signature to `arg`.

        ..  container:: example

            **Example 1.** Adds two time signatures with the same denominator:

            >>> TimeSignature((3, 4)) + TimeSignature((3, 4))
            TimeSignature((6, 4))

        ..  container:: example

            **Example 2.** Adds two time signatures with different
            denominators:

            >>> TimeSignature((3, 4)) + TimeSignature((6, 8))
            TimeSignature((12, 8))

            Returns new time signature in terms of greatest denominator.

        Returns new time signature.
        '''
        if not isinstance(arg, type(self)):
            message = 'must be time signature: {!r}.'
            message = message.format(arg)
            raise Exception(message)
        nonreduced_1 = mathtools.NonreducedFraction(
            self.numerator,
            self.denominator,
            )
        nonreduced_2 = mathtools.NonreducedFraction(
            arg.numerator,
            arg.denominator,
            )
        result = nonreduced_1 + nonreduced_2
        result = type(self)((
            result.numerator,
            result.denominator,
            ))
        return result

    def __copy__(self, *args):
        r'''Copies time signature.

        Returns new time signature.
        '''
        return type(self)(
            (self.numerator, self.denominator),
            partial=self.partial,
            )

    def __eq__(self, arg):
        r'''Is true when `arg` is a time signature with numerator and
        denominator equal to this time signature. Also true when `arg` is a
        tuple with first and second elements equal to numerator and denominator
        of this time signature. Otherwise false.

        Returns true or false.
        '''
        if isinstance(arg, type(self)):
            return (self.numerator == arg.numerator and
                self.denominator == arg.denominator)
        elif isinstance(arg, tuple):
            return self.numerator == arg[0] and self.denominator == arg[1]
        else:
            return False

    def __format__(self, format_specification=''):
        r'''Formats time signature.

        ..  container:: example

            **Example 1.** First time signature:

            ::

                >>> print(format(TimeSignature((3, 8))))
                indicatortools.TimeSignature((3, 8))

        ..  container:: example

            **Example 2.** Second time signature:

            ::

                >>> print(format(TimeSignature((4, 4))))
                indicatortools.TimeSignature((4, 4))

        Returns string.
        '''
        from abjad.tools import systemtools
        if format_specification in ('', 'storage'):
            return systemtools.StorageFormatAgent(self).get_storage_format()
        elif format_specification == 'lilypond':
            return self._lilypond_format
        return str(self)

    def __ge__(self, arg):
        r'''Is true when duration of time signature is greater than or equal to
        duration of `arg`. Otherwise false.

        Returns true or false.
        '''
        if isinstance(arg, type(self)):
            return self.duration >= arg.duration
        else:
            raise TypeError

    def __gt__(self, arg):
        r'''Is true when duration of time signature is greater than duration of
        `arg`. Otherwise false.

        Returns true or false.
        '''
        if isinstance(arg, type(self)):
            return self.duration > arg.duration
        else:
            raise TypeError

    def __hash__(self):
        r'''Hashes time signature.

        Required to be explicitly redefined on Python 3 if __eq__ changes.

        Returns integer.
        '''
        return super(TimeSignature, self).__hash__()

    def __le__(self, arg):
        r'''Is true when duration of time signature is less than duration of
        `arg`. Otherwise false.

        Returns true or false.
        '''
        if isinstance(arg, type(self)):
            return self.duration <= arg.duration
        else:
            raise TypeError

    def __lt__(self, arg):
        r'''Is true when duration of time signature is less than duration of
        `arg`. Otherwise false.

        Returns booelan.
        '''
        if isinstance(arg, type(self)):
            return self.duration < arg.duration
        else:
            raise TypeError

    def __radd__(self, arg):
        r'''Adds `arg` to time signature.

        ..  container:: example

            **Example 1.** Adds integer to first time signature:

            >>> TimeSignature((3, 8)) + TimeSignature((4, 4))
            TimeSignature((11, 8))

        ..  container:: example

            **Example 2.** Adds integer to second time signature:

            >>> TimeSignature((4, 4)) + TimeSignature((3, 8))
            TimeSignature((11, 8))

        Returns new time signature.
        '''
        return self.__add__(arg)

    def __str__(self):
        r'''Gets string representation of time signature.

        ..  container:: example

            **Example 1.** First time signature:

            ::

                >>> str(TimeSignature((3, 8)))
                '3/8'

        ..  container:: example

            **Example 2.** Second time signature:

            ::

                >>> str(TimeSignature((4, 4)))
                '4/4'

        Returns string.
        '''
        return '{}/{}'.format(self.numerator, self.denominator)

    ### PRIVATE METHODS ###

    def _get_format_specification(self):
        storage_format_is_indented = False
        if self.partial is not None or self.suppress is not None:
            storage_format_is_indented = True
        return systemtools.FormatSpecification(
            client=self,
            repr_is_indented=False,
            storage_format_args_values=[self.pair],
            storage_format_kwargs_names=['partial', 'suppress'],
            storage_format_is_indented=storage_format_is_indented,
            )

    ### PUBLIC METHODS ###

    def with_power_of_two_denominator(
        self,
        contents_multiplier=durationtools.Multiplier(1),
        ):
        r'''Makes new time signature equivalent to current
        time signature with power-of-two denominator.

        ..  container:: example

            **Example 1.** Non-power-of-two denominator with power-of-two
            denominator:

                >>> time_signature = TimeSignature((3, 12))
                >>> time_signature.with_power_of_two_denominator()
                TimeSignature((2, 8))

        Returns new time signature.
        '''
        # check input
        contents_multiplier = durationtools.Multiplier(contents_multiplier)

        # save non_power_of_two time_signature and denominator
        non_power_of_two_denominator = self.denominator

        # find power_of_two denominator
        if contents_multiplier == durationtools.Multiplier(1):
            power_of_two_denominator = \
                mathtools.greatest_power_of_two_less_equal(
                    non_power_of_two_denominator)
        else:
            power_of_two_denominator = \
                mathtools.greatest_power_of_two_less_equal(
                    non_power_of_two_denominator, 1)

        # find power_of_two pair
        non_power_of_two_pair = mathtools.NonreducedFraction(self.pair)
        power_of_two_fraction = non_power_of_two_pair.with_denominator(
            power_of_two_denominator)
        power_of_two_pair = power_of_two_fraction.pair

        # return new power_of_two time signature
        return type(self)(power_of_two_pair)

    ### PRIVATE PROPERTIES ###

    @property
    def _contents_repr_string(self):
        return '{}/{}'.format(self.numerator, self.denominator)

    @property
    def _lilypond_format(self):
        if self.suppress:
            return []
        elif self.partial is None:
            return r'\time {}/{}'.format(
                int(self.numerator),
                int(self.denominator),
                )
        else:
            result = []
            duration_string = self.partial.lilypond_duration_string
            partial_directive = r'\partial {}'.format(duration_string)
            result.append(partial_directive)
            string = r'\time {}/{}'.format(
                int(self.numerator),
                int(self.denominator),
                )
            result.append(string)
            return result

    ### PUBLIC PROPERTIES ###

    @property
    def default_scope(self):
        r'''Gets default scope of time signature.

        ..  container:: example

            **Example 1.** First time signature:

            ::

                >>> TimeSignature((3, 8)).default_scope
                <class 'abjad.tools.scoretools.Staff.Staff'>

        ..  container:: example

            **Example 2.** Second time signature:

            ::

                >>> TimeSignature((4, 4)).default_scope
                <class 'abjad.tools.scoretools.Staff.Staff'>

        Returns staff.
        '''
        return self._default_scope

    @property
    def denominator(self):
        r'''Gets denominator of time signature:

        ..  container:: example

            **Example 1.** First time signature:

            ::

                >>> TimeSignature((3, 8)).denominator
                8

        ..  container:: example

            **Example 2.** Second time signature:

            ::

                >>> TimeSignature((4, 4)).denominator
                4

        Set to positive integer.

        Returns positive integer.
        '''
        return self._denominator

    @property
    def duration(self):
        r'''Gets duration of time signature.

        ..  container:: example

            **Example 1.** First time signature:

            ::

                >>> TimeSignature((3, 8)).duration
                Duration(3, 8)

        ..  container:: example

            **Example 2.** Second time signature:

            ::

                >>> TimeSignature((4, 4)).duration
                Duration(1, 1)

        Returns duration.
        '''
        return durationtools.Duration(self.numerator, self.denominator)

    @property
    def has_non_power_of_two_denominator(self):
        r'''Is true when time signature has non-power-of-two denominator.
        Otherwise false.

        ..  container:: example

            **Example 1.** With non-power-of-two denominator:

            ::

                >>> time_signature = TimeSignature((7, 12))
                >>> time_signature.has_non_power_of_two_denominator
                True

        ..  container:: example

            **Example 2.** With power-of-two denominator:

            ::

                >>> time_signature = TimeSignature((3, 8))
                >>> time_signature.has_non_power_of_two_denominator
                False

        Returns true or false.
        '''
        return self._has_non_power_of_two_denominator

    @property
    def implied_prolation(self):
        '''Gets implied prolation of time signature.

        ..  container:: example

            **Example 1.** Implied prolation of time signature with
            power-of-two denominator:

            ::

                >>> TimeSignature((3, 8)).implied_prolation
                Multiplier(1, 1)

        ..  container:: example

            **Example 2.** Implied prolation of time signature
            with non-power-of-two denominator:

            ::

                >>> TimeSignature((7, 12)).implied_prolation
                Multiplier(2, 3)

        Returns multiplier.
        '''
        dummy_duration = durationtools.Duration(1, self.denominator)
        return dummy_duration.implied_prolation

    @property
    def numerator(self):
        r'''Gets numerator of time signature.

        ..  container:: example

            **Example 1.** First time signature:

            ::

                >>> TimeSignature((3, 8)).numerator
                3

        ..  container:: example

            **Example 2.** Second time signature:

            ::

                >>> TimeSignature((4, 4)).numerator
                4

        Set to positive integer.

        Returns positive integer.
        '''
        return self._numerator

    @property
    def pair(self):
        '''Gets numerator / denominator pair corresponding to time siganture.

        ..  container:: example

            **Example 1.** First time signature:

            ::

                >>> TimeSignature((3, 8)).pair
                (3, 8)

        ..  container:: example

            **Example 2.** Second time signature:

            ::

                >>> TimeSignature((4, 4)).pair
                (4, 4)

        Returns pair.
        '''
        return (self.numerator, self.denominator)

    @property
    def partial(self):
        r'''Gets duration of pick-up to time signature.

        ..  container:: example

            **Example 1.** First time signature:

            ::

                >>> TimeSignature((3, 8)).partial is None
                True

        ..  container:: example

            **Example 2.** Second time signature:

            ::

                >>> TimeSignature((4, 4)).partial is None
                True

        Set to duration or none.

        Defaults to none.

        Returns duration or none.
        '''
        return self._partial

    # TODO: make suppress settable only at initialization
    @property
    def suppress(self):
        r'''Is true when time signature should be suppressed in output.
        Otherwise false.

        ..  container:: example

            **Example 1.** First time signature:

            ::

                >>> TimeSignature((3, 8)).suppress is None
                True

        ..  container:: example

            **Example 2.** Second time signature:

            ::

                >>> TimeSignature((4, 4)).suppress is None
                True

        Set to boolean or none.

        Defaults to none.

        Returns boolean or none.
        '''
        return self._suppress

    @suppress.setter
    def suppress(self, expr):
        self._suppress = bool(expr)
