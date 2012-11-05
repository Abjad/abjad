from abjad.tools import durationtools
from abjad.tools import mathtools
from abjad.tools.contexttools.ContextMark import ContextMark


class TimeSignatureMark(ContextMark):
    r'''.. versionadded:: 2.0

    Abjad model of a time signature::

        >>> staff = Staff("c'8 d'8 e'8 f'8")

    ::

        >>> contexttools.TimeSignatureMark((4, 8))(staff[0])
        TimeSignatureMark((4, 8))(c'8)

    ::

        >>> f(staff)
        \new Staff {
            \time 4/8
            c'8
            d'8
            e'8
            f'8
        }

    Abjad time signature marks target **staff context** by default.

    Initialize time signature marks to **score context** like this::

        >>> contexttools.TimeSignatureMark((4, 8), target_context=Score)
        TimeSignatureMark((4, 8), target_context=Score)

    .. note:: add more initializer examples.

    .. note:: add example of `suppress` keyword.

    .. note:: turn `suppress` into managed attribute.

    Return time signature object.
    '''

    ### CLASS ATTRIBUTES ###

    _default_mandatory_input_arguments = ((4, 8), )

    _format_slot = 'opening'

    ### INITIALIZER ###

    def __init__(self, *args, **kwargs):
        from abjad.tools.stafftools.Staff import Staff
        target_context = kwargs.get('target_context', None)
        ContextMark.__init__(self, target_context=target_context)
        if self.target_context is None:
            self._target_context = Staff
        if self._target_context == Staff:
            self._has_default_target_context = True
        else:
            self._has_default_target_context = False

        partial, suppress = None, None

        # initialize numerator and denominator from *args
        if len(args) == 1 and isinstance(args[0], type(self)):
            time_signature = args[0]
            numerator, denominator = time_signature.numerator, time_signature.denominator
            partial = time_signature.partial
            suppress = time_signature.suppress
        elif len(args) == 1 and isinstance(args[0], durationtools.Duration):
            numerator, denominator = args[0].numerator, args[0].denominator
        elif len(args) == 1 and isinstance(args[0], tuple):
            numerator, denominator = args[0][0], args[0][1]
        elif len(args) == 1 and hasattr(args[0], 'numerator') and hasattr(args[0], 'denominator'):
            numerator, denominator = args[0].numerator, args[0].denominator 
        else:
            raise TypeError('invalid time_signature initialization: {!r}.'.format(args))
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
        self._has_non_power_of_two_denominator = not mathtools.is_nonnegative_integer_power_of_two(
            self.denominator)

    ### SPECIAL METHODS ###

    def __copy__(self, *args):
        return type(self)((self.numerator, self.denominator),
            partial = self.partial, target_context = self.target_context)

    # note that this can not be defined on superclass
    __deepcopy__ = __copy__

    def __eq__(self, arg):
        if isinstance(arg, type(self)):
            return self.numerator == arg.numerator and self.denominator == arg.denominator
        elif isinstance(arg, tuple):
            return self.numerator == arg[0] and self.denominator == arg[1]
        else:
            return False

    def __ge__(self, arg):
        if isinstance(arg, type(self)):
            return self.duration >= arg.duration
        else:
            raise TypeError

    # TODO: define __getnewargs__?

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
        if self._has_default_target_context:
            return '%s((%s, %s)%s)%s' % (type(self).__name__, self.numerator,
                self.denominator, self._partial_repr_string, self._attachment_repr_string)
        else:
            return '%s((%s, %s)%s, target_context=%s)%s' % (
                type(self).__name__, self.numerator,
                self.denominator, self._partial_repr_string, self._target_context_name, 
                self._attachment_repr_string)

    def __str__(self):
        return '%s/%s' % (self.numerator, self.denominator)

    ### PRIVATE PROPERTIES ###

    @property
    def _contents_repr_string(self):
        return '%s/%s' % (self.numerator, self.denominator)

    @property
    def _keyword_argument_names(self):
        return (
            'partial',
            'suppress',
            )

    @property
    def _mandatory_argument_values(self):
        return (self.pair, )

    ### READ-ONLY PUBLIC PROPERTIES ###

    @property
    def duration(self):
        r'''Time signature mark duration::

            >>> contexttools.TimeSignatureMark((3, 8)).duration
            Duration(3, 8)

        Return duration.
        '''
        return durationtools.Duration(self.numerator, self.denominator)

    @property
    def effective_context(self):
        r'''Time signature mark effective context.

        Return none when time signature mark is not yet attached::

            >>> time_signature = contexttools.TimeSignatureMark((3, 8))

        ::

            >>> time_signature.effective_context is None
            True

        Return context when time signature mark is attached::

            >>> staff = Staff()
            >>> time_signature.attach(staff)
            TimeSignatureMark((3, 8))(Staff{})

        ::

            >>> time_signature.effective_context 
            Staff{}

        Return context or none.
        '''
        return ContextMark.effective_context.fget(self)

    @property
    def has_non_power_of_two_denominator(self):
        r'''True when time signature mark has non-power-of-two denominator::

            >>> contexttools.TimeSignatureMark((7, 12)).has_non_power_of_two_denominator
            True

        Otherwise false::

            >>> contexttools.TimeSignatureMark((3, 8)).has_non_power_of_two_denominator
            False

        Return boolean.
        '''
        return self._has_non_power_of_two_denominator

    @property
    def implied_prolation(self):
        '''.. versionadded:: 2.11

        Time signature mark implied prolation.

        Example 1. Implied prolation of time signature with power-of-two denominator::

            >>> contexttools.TimeSignatureMark((3, 8)).implied_prolation
            Multiplier(1, 1)
        
        Example 2. Implied prolation of time signature with non-power-of-two denominator::

            >>> contexttools.TimeSignatureMark((7, 12)).implied_prolation
            Multiplier(2, 3)

        Return multiplier.
        '''
        dummy_duration = durationtools.Duration(1, self.denominator)
        return dummy_duration.implied_prolation

    @property
    def lilypond_format(self):
        r'''Time signature mark LilyPond format::

            >>> contexttools.TimeSignatureMark((3, 8)).lilypond_format
            '\\time 3/8'

        Return string.
        '''
        if self.suppress:
            return []
        elif self.partial is None:
            return r'\time %s/%s' % (self.numerator, self.denominator)
        else:
            result = []
            duration_string = self.partial.lilypond_duration_string
            partial_directive = r'\partial %s' % duration_string
            result.append(partial_directive)
            result.append(r'\time %s/%s' % (self.numerator, self.denominator))
            return result

    @property
    def pair(self):
        '''.. versionadded:: 2.8

        Time signature numerator / denominator pair::

            >>> contexttools.TimeSignatureMark((3, 8)).pair
            (3, 8)

        Return pair.
        '''
        return (self.numerator, self.denominator)

    @property
    def start_component(self):
        r'''Time signature mark start component.

        Return none when time signature mark is not yet attached::

            >>> time_signature = contexttools.TimeSignatureMark((3, 8))
            >>> time_signature.start_component is None
            True

        Return component when time signature mark is attached::

            >>> staff = Staff()
            >>> time_signature.attach(staff)
            TimeSignatureMark((3, 8))(Staff{})

        ::

            >>> time_signature.start_component
            Staff{}

        Return component or none.
        '''
        return ContextMark.start_component.fget(self)

    @property
    def storage_format(self):
        r'''Time signature mark storage format::

            >>> print contexttools.TimeSignatureMark((3, 8)).storage_format
            contexttools.TimeSignatureMark(
                (3, 8)
                )

        Return string.
        '''
        return ContextMark.storage_format.fget(self)

    @property
    def target_context(self):
        r'''Time signature mark target context::

            >>> contexttools.TimeSignatureMark((3, 8)).target_context
            <class 'abjad.tools.stafftools.Staff.Staff.Staff'>

        Time signature marks target the staff context by default.

        This can be changed at initialization.
        
        Return class.
        '''
        return ContextMark.target_context.fget(self)

    ### READ / WRITE PUBLIC PROPERTIES ###

    @apply
    def denominator():
        def fget(self):
            r'''Get denominator of time signature mark::

                >>> time_signature = contexttools.TimeSignatureMark((3, 8))

            ::

                >>> time_signature.denominator
                8

            Set denominator of time signature mark::

                >>> time_signature.denominator = 16

            ::

                >>> time_signature.denominator
                16

            Return integer.
            '''
            return self._denominator
        def fset(self, denominator):
            assert isinstance(denominator, int)
            self._denominator = denominator
        return property(**locals())

    @apply
    def numerator():
        def fget(self):
            '''Get numerator of time signature mark::

                >>> time_signature = contexttools.TimeSignatureMark((3, 8))
                >>> time_signature.numerator
                3

            Set numerator of time signature mark::

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

    @apply
    def partial():
        def fget(self):
            '''Get partial measure pick-up of time signature mark::

                >>> time_signature = contexttools.TimeSignatureMark(
                ...     (3, 8), partial=Duration(1, 8))
                >>> time_signature.partial
                Duration(1, 8)

            Set partial measure pick-up of time signature mark::

                >>> time_signature.partial = Duration(1, 4)
                >>> time_signature.partial
                Duration(1, 4)

            Set duration or none.
            '''
            return self._partial
        def fset(self, partial):
            if partial is not None:
                partial = durationtools.Duration(partial)
            self._partial = partial
        return property(**locals())

    ### PUBLIC METHODS ###

    # Time signature marks do not check for other conflicting time signature marks at attachment.
    # The reason for this is that voodoo is being done to time signature marks elsewhere in the code.
    # This is less than optimal and someday time signature marks should check for conflicts at attachment.
    def attach(self, start_component):
        r'''Attach time signature mark to `start_component`::

            >>> time_signature = contexttools.TimeSignatureMark((3, 8))
            >>> staff = Staff()

        ::

            >>> time_signature.attach(staff)
            TimeSignatureMark((3, 8))(Staff{})

        Return time signature mark.
        '''
        from abjad.tools import contexttools
        from abjad.tools import marktools
        klasses = (type(self), )
        if contexttools.is_component_with_context_mark_attached(start_component, klasses):
            raise ExtraMarkError('component already has context mark attached.')
        return marktools.Mark.attach(self, start_component)

    def detach(self):
        r'''Detach time signature mark::

            >>> time_signature = contexttools.TimeSignatureMark((3, 8))
            >>> staff = Staff()

        ::

            >>> time_signature.attach(staff)
            TimeSignatureMark((3, 8))(Staff{})

        ::

            >>> time_signature.detach()
            TimeSignatureMark((3, 8))

        Return time signature mark.
        '''
        return ContextMark.detach(self)

    def with_power_of_two_denominator(self, contents_multiplier=durationtools.Multiplier(1)):
        r'''Create new time signature equivalent to current
        time signature with power-of-two denominator.

            >>> time_signature = contexttools.TimeSignatureMark((3, 12))

        ::

            >>> time_signature.with_power_of_two_denominator()
            TimeSignatureMark((2, 8))

        Return new time signature mark.
        '''
        # check input
        contents_multiplier = durationtools.Multiplier(contents_multiplier)
    
        # save non_power_of_two time_signature and denominator
        non_power_of_two_denominator = self.denominator

        # find power_of_two denominator
        if contents_multiplier == durationtools.Multiplier(1):
            power_of_two_denominator = mathtools.greatest_power_of_two_less_equal(
                non_power_of_two_denominator)
        else:
            power_of_two_denominator = mathtools.greatest_power_of_two_less_equal(
                non_power_of_two_denominator, 1)

        # find power_of_two pair
        non_power_of_two_pair = mathtools.NonreducedFraction(self.pair)
        power_of_two_pair = non_power_of_two_pair.with_denominator(power_of_two_denominator)

        # return new power_of_two time signature mark
        return type(self)(power_of_two_pair)
