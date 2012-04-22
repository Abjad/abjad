from abjad.tools import contexttools
from abjad.tools import durationtools
from abjad.tools.containertools.Container import Container
from abjad.tools.measuretools.Measure._MeasureFormatter import _MeasureFormatter
import copy


class Measure(Container):
    r'''.. versionadded:: 1.1

    Abjad model of a measure::

        abjad> measure = Measure((4, 8), "c'8 d' e' f'")

    ::

        abjad> measure
        Measure(4/8, [c'8, d'8, e'8, f'8])

    ::

        abjad> f(measure)
        {
            \time 4/8
            c'8
            d'8
            e'8
            f'8
        }

    Return measure object.
    '''

    ### CLASS ATTRIBUTES ###

    __slots__ = ('_automatically_update_time_signature', '_measure_number', )

    ### INITIALIZER ###

    def __init__(self, meter, music=None, **kwargs):
        Container.__init__(self, music)
        self._automatically_update_time_signature = False
        self._formatter = _MeasureFormatter(self)
        self._measure_number = None
        time_signature = contexttools.TimeSignatureMark(meter)
        time_signature.attach(self)
        self._initialize_keyword_values(**kwargs)

    ### SPECIAL METHODS ###

    def __add__(self, arg):
        '''Add two measures together in-score or outside-of-score.
        Wrapper around measuretools.fuse_measures.
        '''
        assert isinstance(arg, type(self))
        from abjad.tools import measuretools
        new = measuretools.fuse_measures([self, arg])
        return new

    # essentially the same as Container.__copy__.
    # the definition given here adds one line to remove
    # time signature immediately after instantiation
    # because the mark-copying code will then provide time signature.
    def __copy__(self, *args):
        from abjad.tools import marktools
        new = type(self)(*self.__getnewargs__())
        # only this line differs from Container.__copy__
        contexttools.detach_time_signature_marks_attached_to_component(new)
        if getattr(self, '_override', None) is not None:
            new._override = copy.copy(self.override)
        if getattr(self, '_set', None) is not None:
            new._set = copy.copy(self.set)
        for mark in marktools.get_marks_attached_to_component(self):
            new_mark = copy.copy(mark)
            new_mark.attach(new)
        new.is_parallel = self.is_parallel
        return new

    def __delitem__(self, i):
        '''Container item deletion with optional time signature adjustment.
        '''
        old_time_signature = contexttools.get_effective_time_signature(self)
        old_denominator = getattr(old_time_signature, 'denominator', None)
        Container.__delitem__(self, i)
        if self.automatically_update_time_signature:
            naive_meter = self.preprolated_duration
            better_meter = durationtools.rational_to_duration_pair_with_specified_integer_denominator(
                naive_meter, old_denominator)
            better_meter = contexttools.TimeSignatureMark(better_meter)
            contexttools.detach_time_signature_marks_attached_to_component(self)
            better_meter.attach(self)

    def __getnewargs__(self):
        time_signature = contexttools.get_effective_time_signature(self)
        return (time_signature.pair, )

    def __repr__(self):
        '''String form of measure with parentheses for interpreter display.
        '''
        class_name = type(self).__name__
        forced_meter = contexttools.get_time_signature_mark_attached_to_component(self)
        summary = self._summary
        length = len(self)
        if forced_meter and length:
            return '%s(%s, [%s])' % (class_name, forced_meter, summary)
        elif forced_meter:
            return '%s(%s)' % (class_name, forced_meter)
        elif length:
            return '%s([%s])' % (class_name, summary)
        else:
            return '%s()' % class_name

    def __str__(self):
        '''String form of measure with pipes for single string display.
        '''
        forced_meter = contexttools.get_effective_time_signature(self)
        summary = self._summary
        length = len(self)
        if forced_meter and length:
            return '|%s, %s|' % (forced_meter, summary)
        elif forced_meter:
            return '|%s|' % forced_meter
        elif length:
            return '|%s|' % summary
        else:
            return '| |'

    ### READ-ONLY PRIVATE PROPERTIES ###

    @property
    def _compact_representation(self):
        '''Display form of measure used for spanners to display
        potentially many spanned measures one after the other.
        '''
        return '|%s(%s)|' % (contexttools.get_effective_time_signature(self), len(self))

    ### READ-ONLY PUBLIC PROPERTIES ###

    @property
    def is_binary(self):
        '''True when measure time signature denominator is an integer power of 2::

            abjad> measure = Measure((5, 8), "c'8 d' e' f' g'")
            abjad> measure.is_binary
            True

        Otherwise false::

            abjad> measure = Measure((5, 9), "c'8 d' e' f' g'")
            abjad> measure.is_binary
            False

        Return boolean.
        '''
        return not self.is_nonbinary

    @property
    def is_full(self):
        '''True when prolated duration equals time signature duration::

            abjad> measure = Measure((4, 8), "c'8 d'8 e'8 f'8")

        ::

            abjad> measure.is_full
            True

        Otherwise false.

        Return boolean.
        '''
        return contexttools.get_effective_time_signature(self).duration == self.preprolated_duration

    @property
    def is_nonbinary(self):
        '''True when measure time signature denominator is not an integer power of 2::

            abjad> measure = Measure((5, 9), "c'8 d' e' f' g'")
            abjad> measure.is_binary
            True
    
        Otherwise false::

            abjad> measure = Measure((5, 8), "c'8 d' e' f' g'")
            abjad> measure.is_binary
            True

        Return boolean.
        '''
        return contexttools.get_effective_time_signature(self).is_nonbinary

    @property
    def is_overfull(self):
        '''.. versionadded:: 1.1

        True when prolated duration is greater than time signature duration::

            abjad> measure = Measure((3, 4), "c'4 d' e' f'")

        ::

            abjad> measure.is_overfull
            True

        Otherwise false.

        Return boolean.
        '''
        return contexttools.get_effective_time_signature(self).duration < self.prolated_duration

    @property
    def is_underfull(self):
        '''.. versionadded:: 1.1

        True when prolated duration is less than time signature duration::

            abjad> measure = Measure((3, 4), "c'4 d'")

        ::

            abjad> measure.is_underfull
            True

        Otherwise false.

        Return boolean.
        '''
        return self.prolated_duration < contexttools.get_effective_time_signature(self).duration

    @property
    def measure_number(self):
        r'''1-indexed measure number::

            abjad> staff = Staff()
            abjad> staff.append(Measure((3, 4), "c' d' e'"))
            abjad> staff.append(Measure((2, 4), "f' g'"))

        ::

            abjad> f(staff)
            \new Staff {
                {
                    \time 3/4
                    c'4
                    d'4
                    e'4
                }
                {
                    \time 2/4
                    f'4
                    g'4
                }
            }

        ::

            abjad> staff[0].measure_number
            1

        ::

            abjad> staff[1].measure_number
            2

        Return positive integer.
        '''
        self._update_prolated_offset_values_of_entire_score_tree_if_necessary()
        return self._measure_number

    @property
    def multiplier(self):
        '''Multiplier of measure time signature::

            abjad> measure = Measure((5, 12), "c'8 d' e' f' g'")

        ::

            abjad> measure.multiplier
            Fraction(2, 3)

        Return fraction.
        '''
        return contexttools.get_effective_time_signature(self).multiplier

    @property
    def preprolated_duration(self):
        '''Preprolated duration of measure::

            abjad> measure = Measure((5, 12), "c'8 d' e' f' g'")

        ::

            abjad> measure.preprolated_duration
            Duration(5, 12)

        Equal measure contents duration times time signature multiplier.

        Return duration.
        '''
        from abjad.tools import contexttools
        return contexttools.get_effective_time_signature(self).multiplier * self.contents_duration

    ### READ / WRITE PUBLIC PROPERTIES ###

    @apply
    def automatically_update_time_signature():
        def fget(self):
            '''..versionadded:: 2.9

            Read / write flag to indicate whether time signature
            should update automatically following contents-changing operations
            like ``append()``, ``extend()``, ``pop()``, ``del()`` and so on.
            
            Default to false.

            Return boolean.
            '''
            return self._automatically_update_time_signature
        def fset(self, expr):
            assert isinstance(expr, bool)
            self._automatically_update_time_signature = expr
        return property(**locals()) 
