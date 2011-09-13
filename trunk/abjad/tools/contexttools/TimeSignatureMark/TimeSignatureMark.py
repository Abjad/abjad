from abjad.tools import durationtools
from abjad.tools import mathtools
from abjad.tools.contexttools.ContextMark import ContextMark
from abjad.tools import durationtools
import numbers


class TimeSignatureMark(ContextMark):
    r'''.. versionadded:: 2.0

    Abjad model of a time signature::

        abjad> staff = Staff("c'8 d'8 e'8 f'8")

    ::

        abjad> contexttools.TimeSignatureMark((4, 8))(staff[0])
        TimeSignatureMark((4, 8))(c'8)

    ::

        abjad> f(staff)
        \new Staff {
            \time 4/8
            c'8
            d'8
            e'8
            f'8
        }


    Abjad time signature marks target **staff context** by default.

    Initialize time signature marks to **score context** like this::

        abjad> contexttools.TimeSignatureMark((4, 8), target_context = Score)
        TimeSignatureMark((4, 8), target_context = Score)

    Time signatures are immutable.
    '''

    _format_slot = 'opening'

    #__slots__ = ('_denominator', '_duration', '_format_slot', '_multiplier',
    #    '_is_nonbinary', '_numerator', '_partial', )

    def __init__(self, *args, **kwargs):
        from abjad.tools.stafftools.Staff import Staff
        target_context = kwargs.get('target_context', None)
        ContextMark.__init__(self, target_context = target_context)
        if self.target_context is None:
            self._target_context = Staff
        if self._target_context == Staff:
            self._has_default_target_context = True
        else:
            self._has_default_target_context = False
        # initialize numerator and denominator from *args
        if len(args) == 1 and isinstance(args[0], type(self)):
            time_signature = args[0]
            numerator, denominator = time_signature.numerator, time_signature.denominator
        elif len(args) == 1 and isinstance(args[0], durationtools.Duration):
            numerator, denominator = args[0].numerator, args[0].denominator
        elif len(args) == 1 and isinstance(args[0], tuple):
            numerator, denominator = args[0][0], args[0][1]
        # removed to bring initialization in line with rests and skips:
        #elif len(args) == 2 and all([isinstance(x, int) for x in args]):
        #    numerator, denominator = args[0], args[1]
        else:
            raise TypeError('invalid time_signature initialization.')
        self._numerator = numerator
        self._denominator = denominator

        # initialize partial from **kwargs
        partial = kwargs.get('partial', None)
        if not isinstance(partial, (type(None), durationtools.Duration)):
            raise TypeError
        self._partial = partial
        if partial is not None:
            self._partial_repr_string = ', partial = %r' % self._partial
        else:
            self._partial_repr_string = ''

        # initialize suppress from kwargs
        suppress = kwargs.get('suppress', None)
        if not isinstance(suppress, (bool, type(None))):
            raise TypeError
        self.suppress = suppress

        # initialize derived attributes
        _multiplier = durationtools.positive_integer_to_implied_prolation_multipler(self.denominator)
        self._multiplier = _multiplier
        self._is_nonbinary = not mathtools.is_nonnegative_integer_power_of_two(self.denominator)

    ### OVERLOADS ###

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
            return '%s((%s, %s)%s, target_context = %s)%s' % (
                type(self).__name__, self.numerator,
                self.denominator, self._partial_repr_string, self._target_context_name, 
                self._attachment_repr_string)

    def __str__(self):
        return '%s/%s' % (self.numerator, self.denominator)

    ### PRIVATE ATTRIBUTES ###

    @property
    def _contents_repr_string(self):
        return '%s/%s' % (self.numerator, self.denominator)

    ### PUBLIC ATTRIBUTES ###

    @apply
    def denominator():
        def fget(self):
            r'''Get denominator of time signature mark::

                abjad> time_signature = contexttools.TimeSignatureMark((3, 8))
                abjad> time_signature
                TimeSignatureMark((3, 8))
                abjad> time_signature.denominator
                8

            Set denominator of time signature mark::

                abjad> time_signature.denominator = 16
                abjad> time_signature.denominator
                16

            Return integer.
            '''
            return self._denominator
        def fset(self, denominator):
            assert isinstance(denominator, int)
            self._denominator = denominator
        return property(**locals())

    @property
    def duration(self):
        r'''Read-only duration of time signature mark::

            abjad> time_signature = contexttools.TimeSignatureMark((3, 8))
            abjad> time_signature.duration
            Duration(3, 8)

        Return fraction.
        '''
        return durationtools.Duration(self.numerator, self.denominator)

    @property
    def format(self):
        r'''Read-only LilyPond format of time signature mark::

            abjad> time_signature = contexttools.TimeSignatureMark((3, 8))
            abjad> time_signature.format
            '\\time 3/8'

        Return string.
        '''
        if self.suppress:
            return []
        elif self.partial is None:
            return r'\time %s/%s' % (self.numerator, self.denominator)
        else:
            result = []
            result.append(r'\time %s/%s' % (self.numerator, self.denominator))
            duration_string = durationtools.assignable_rational_to_lilypond_duration_string(self.partial)
            partial_directive = r'\partial %s' % duration_string
            result.append(partial_directive)
            return result

    @property
    def multiplier(self):
        r'''Read-only multiplier of time signature mark::

            abjad> time_signature = contexttools.TimeSignatureMark((3, 8))
            abjad> time_signature.multiplier
            Fraction(1, 1)

        Return fraction.
        '''
        return self._multiplier

    @apply
    def numerator():
        def fget(self):
            '''Get numerator of time signature mark::

                abjad> time_signature = contexttools.TimeSignatureMark((3, 8))
                abjad> time_signature.numerator
                3

            Set numerator of time signature mark::

                abjad> time_signature.numerator = 4
                abjad> time_signature.numerator
                4

            Set integer.
            '''
            return self._numerator
        def fset(self, numerator):
            assert isinstance(numerator, int)
            self._numerator = numerator
        return property(**locals())

    @property
    def is_nonbinary(self):
        r'''Read-only indicator true when time siganture mark is nonbinary::

            abjad> time_signature = contexttools.TimeSignatureMark((3, 8))
            abjad> time_signature.is_nonbinary
            False

        Return boolean.
        '''
        return self._is_nonbinary

    @apply
    def partial():
        def fget(self):
            '''Get partial measure pick-up of time signature mark::

                abjad> time_signature = contexttools.TimeSignatureMark((3, 8), partial = Duration(1, 8))
                abjad> time_signature.partial
                Duration(1, 8)

            Set partial measure pick-up of time signature mark::

                abjad> time_signature.partial = Duration(1, 4)
                abjad> time_signature.partial
                Duration(1, 4)

            Set fraction or none.
            '''
            return self._partial
        def fset(self, partial):
            assert isinstance(partial, (numbers.Number, type(None)))
            self._partial = partial
        return property(**locals())
