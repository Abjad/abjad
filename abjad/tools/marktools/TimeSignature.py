# -*- encoding: utf-8 -*-
from abjad.tools import durationtools
from abjad.tools import mathtools
from abjad.tools.marktools.ContextMark import ContextMark


# TODO: add more initializer examples.
# TODO: add example of `suppress` keyword.
# TODO: turn `suppress` into managed attribute.
class TimeSignature(ContextMark):
    r'''A time signature.

    ::

        >>> staff = Staff("c'8 d'8 e'8 f'8")
        >>> time_signature = TimeSignature((4, 8))
        >>> attach(time_signature, staff[0])
        >>> show(staff) # doctest: +SKIP

    ..  doctest::

        >>> f(staff)
        \new Staff {
            \time 4/8
            c'8
            d'8
            e'8
            f'8
        }

    Time signatures attach to the **staff context** by default.

    Attach time signatures to the **score context** like this:

    ::

        >>> staff = Staff("c'8 d'8 e'8 f'8")
        >>> time_signature = TimeSignature((4, 8))
        >>> attach(time_signature, staff[0], target_context=Score)
        >>> show(staff) # doctest: +SKIP

    '''

    ### CLASS VARIABLES ###

    _default_positional_input_arguments = (
        (4, 8),
        )

    _format_slot = 'opening'

    ### INITIALIZER ###

    def __init__(self, *args, **kwargs):
        ContextMark.__init__(self)
        partial, suppress = None, None
        # initialize numerator and denominator from *args
        if len(args) == 1 and isinstance(args[0], type(self)):
            time_signature = args[0]
            numerator = time_signature.numerator
            denominator = time_signature.denominator
            partial = time_signature.partial
            suppress = time_signature.suppress
        elif len(args) == 1 and isinstance(args[0], durationtools.Duration):
            numerator, denominator = args[0].numerator, args[0].denominator
        elif len(args) == 1 and isinstance(args[0], tuple):
            numerator, denominator = args[0][0], args[0][1]
        elif len(args) == 1 and hasattr(args[0], 'numerator') and \
            hasattr(args[0], 'denominator'):
            numerator, denominator = args[0].numerator, args[0].denominator
        else:
            message = 'invalid time_signature initialization: {!r}.'
            message = message.format(args)
            raise TypeError(message)
        self._numerator = numerator
        self._denominator = denominator
        # initialize partial from **kwargs
        partial = partial or kwargs.get('partial', None)
        if not isinstance(partial, (type(None), durationtools.Duration)):
            raise TypeError
        self._partial = partial
        if partial is not None:
            self._partial_repr_string = ', partial=%r' % self._partial
        else:
            self._partial_repr_string = ''
        # initialize suppress from kwargs
        suppress = suppress or kwargs.get('suppress', None)
        if not isinstance(suppress, (bool, type(None))):
            raise TypeError
        self.suppress = suppress
        # initialize derived attributes
        self._multiplier = self.implied_prolation
        self._has_non_power_of_two_denominator = \
            not mathtools.is_nonnegative_integer_power_of_two(
            self.denominator)

    ### SPECIAL METHODS ###

    def __copy__(self, *args):
        return type(self)(
            (self.numerator, self.denominator),
            partial=self.partial, 
            )

    def __eq__(self, arg):
        if isinstance(arg, type(self)):
            return self.numerator == arg.numerator and \
                self.denominator == arg.denominator
        elif isinstance(arg, tuple):
            return self.numerator == arg[0] and self.denominator == arg[1]
        else:
            return False

    def __format__(self, format_specification=''):
        r'''Formats time signature.

        ::

            >>> print format(TimeSignature((3, 8)))
            marktools.TimeSignature(
                (3, 8)
                )

        Returns string.
        '''
        superclass = super(TimeSignature, self)
        return superclass.__format__(format_specification=format_specification)

    def __ge__(self, arg):
        if isinstance(arg, type(self)):
            return self.duration >= arg.duration
        else:
            raise TypeError

    def __gt__(self, arg):
        if isinstance(arg, type(self)):
            return self.duration > arg.duration
        else:
            raise TypeError

    def __le__(self, arg):
        if isinstance(arg, type(self)):
            return self.duration <= arg.duration
        else:
            raise TypeError

    def __lt__(self, arg):
        if isinstance(arg, type(self)):
            return self.duration < arg.duration
        else:
            raise TypeError

    def __ne__(self, arg):
        return not self == arg

    def __nonzero__(self):
        return True

    def __repr__(self):
        result = '{}(({}, {}){}){}'
        result = result.format(
            type(self).__name__, 
            self.numerator,
            self.denominator, 
            self._partial_repr_string, 
            self._attachment_repr_string,
            )
        return result

    def __str__(self):
        return '{}/{}'.format(self.numerator, self.denominator)

    ### PRIVATE PROPERTIES ###

    @property
    def _contents_repr_string(self):
        return '{}/{}'.format(self.numerator, self.denominator)

    @property
    def _keyword_argument_names(self):
        return (
            'partial',
            'suppress',
            )

    @property
    def _lilypond_format(self):
        if self.suppress:
            return []
        elif self.partial is None:
            return r'\time {}/{}'.format(self.numerator, self.denominator)
        else:
            result = []
            duration_string = self.partial.lilypond_duration_string
            partial_directive = r'\partial {}'.format(duration_string)
            result.append(partial_directive)
            string =r'\time {}/{}'.format(self.numerator, self.denominator)
            result.append(string)
            return result

    @property
    def _positional_argument_values(self):
        return (self.pair, )

    ### PUBLIC PROPERTIES ###

    @apply
    def denominator():
        def fget(self):
            r'''Gets and sets time signature denominator.

            ::

                >>> time_signature = TimeSignature((3, 8))

            ::

                >>> time_signature.denominator
                8

            Sets time signature denominator:

            ::

                >>> time_signature.denominator = 16

            ::

                >>> time_signature.denominator
                16

            Returns integer.
            '''
            return self._denominator
        def fset(self, denominator):
            assert isinstance(denominator, int)
            self._denominator = denominator
        return property(**locals())

    @property
    def duration(self):
        r'''Time signature duration.

        ::

            >>> TimeSignature((3, 8)).duration
            Duration(3, 8)

        Returns duration.
        '''
        return durationtools.Duration(self.numerator, self.denominator)

    @property
    def has_non_power_of_two_denominator(self):
        r'''True when time signature has non-power-of-two denominator.

        ::

            >>> time_signature = TimeSignature((7, 12))
            >>> time_signature.has_non_power_of_two_denominator
            True

        Otherwise false:

        ::

            >>> time_signature = TimeSignature((3, 8))
            >>> time_signature.has_non_power_of_two_denominator
            False

        Returns boolean.
        '''
        return self._has_non_power_of_two_denominator

    @property
    def implied_prolation(self):
        '''Time signature implied prolation.

        ..  container:: example

            **Example 1.** Implied prolation of time signature 
            with power-of-two denominator:

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

    @apply
    def numerator():
        def fget(self):
            r'''Gets and sets time signature numerator.

            ::

                >>> time_signature = TimeSignature((3, 8))
                >>> time_signature.numerator
                3

            Sets time signature numerator:

            ::

                >>> time_signature.numerator = 4
                >>> time_signature.numerator
                4

            Set integer.
            '''
            return self._numerator
        def fset(self, numerator):
            assert isinstance(numerator, int)
            self._numerator = numerator
        return property(**locals())

    @property
    def pair(self):
        '''Time signature numerator / denominator pair:

        ::

            >>> TimeSignature((3, 8)).pair
            (3, 8)

        Returns pair.
        '''
        return (self.numerator, self.denominator)

    @apply
    def partial():
        def fget(self):
            r'''Gets partial measure pick-up of time signature.

            ::

                >>> duration = Duration(1, 8)
                >>> time_signature = TimeSignature((3, 8), partial=duration)
                >>> time_signature.partial
                Duration(1, 8)

            Sets partial measure pick-up of time signature.

            ::

                >>> time_signature.partial = Duration(1, 4)
                >>> time_signature.partial
                Duration(1, 4)

            Returns duration.
            '''
            return self._partial
        def fset(self, partial):
            if partial is not None:
                partial = durationtools.Duration(partial)
            self._partial = partial
        return property(**locals())

    ### PUBLIC METHODS ###

    def _attach(self, start_component):
        from abjad.tools import marktools
        classes = (type(self), )
        if start_component._has_mark(mark_classes=classes):
            message = 'component already has context mark attached.'
            raise ExtraMarkError(message)
        return marktools.Mark._attach(self, start_component)

    def with_power_of_two_denominator(self, 
        contents_multiplier=durationtools.Multiplier(1)):
        r'''Create new time signature equivalent to current
        time signature with power-of-two denominator.

            >>> time_signature = TimeSignature((3, 12))

        ::

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
        power_of_two_pair = non_power_of_two_pair.with_denominator(
            power_of_two_denominator)

        # return new power_of_two time signature
        return type(self)(power_of_two_pair)
