from abjad.tools import contexttools
from abjad.tools import durationtools
from abjad.tools.containertools.Container import Container
from abjad.tools.measuretools.Measure._MeasureFormatter import _MeasureFormatter
import copy


class Measure(Container):
    r'''.. versionadded:: 1.1

    Abjad model of a measure::

        abjad> measure = Measure((4, 8), "c'8 d'8 e'8 f'8")

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

    __slots__ = ('_measure_number', )

    def __init__(self, meter, music = None, **kwargs):
        Container.__init__(self, music)
        self._formatter = _MeasureFormatter(self)
        self._measure_number = None
        time_signature = contexttools.TimeSignatureMark(meter)
        time_signature.attach(self)
        self._initialize_keyword_values(**kwargs)

    ### OVERLOADS ###

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
        '''Container deletion with meter adjustment.
        '''
        try:
            old_denominator = contexttools.get_effective_time_signature(self).denominator
        except AttributeError:
            pass
        Container.__delitem__(self, i)
        try:
            naive_meter = self.preprolated_duration
            better_meter = durationtools.rational_to_duration_pair_with_specified_integer_denominator(
                naive_meter, old_denominator)
            better_meter = contexttools.TimeSignatureMark(better_meter)
            contexttools.detach_time_signature_marks_attached_to_component(self)
            better_meter.attach(self)
        except (AttributeError, UnboundLocalError):
            pass

    def __getnewargs__(self):
        time_signature = contexttools.get_effective_time_signature(self)
        pair = (time_signature.numerator, time_signature.denominator)
        return (pair, )

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

    ### PRIVATE ATTRIBUTES ###

    @property
    def _compact_representation(self):
        '''Display form of measure used for spanners to display
        potentially many spanned measures one after the other.
        '''
        return '|%s(%s)|' % (contexttools.get_effective_time_signature(self), len(self))

    ### PUBLIC ATTRIBUTES ###

    @property
    def is_binary(self):
        return not self.is_nonbinary

    @property
    def is_full(self):
        '''True when meter matches duration of measure::

            abjad> measure = Measure((4, 8), "c'8 d'8 e'8 f'8")

        ::

            abjad> measure.is_full
            True

        False otherwise::

            abjad> measure = Measure((4, 8), "c'8 d'8 e'8")

        ::

            abjad> measure.is_full
            False

        Return boolean.
        '''
        return contexttools.get_effective_time_signature(self).duration == self.preprolated_duration

    @property
    def is_nonbinary(self):
        return contexttools.get_effective_time_signature(self).is_nonbinary

    @property
    def is_overfull(self):
        '''.. versionadded:: 1.1

        True when prolated duration is greater than
        effective meter duration.
        '''
        return contexttools.get_effective_time_signature(self).duration < self.prolated_duration

    @property
    def is_underfull(self):
        '''.. versionadded:: 1.1

        True when prolated duration is less than
        effective meter duration.
        '''
        return self.prolated_duration < contexttools.get_effective_time_signature(self).duration

    @property
    def measure_number(self):
        self._update_prolated_offset_values_of_entire_score_tree_if_necessary()
        return self._measure_number

    @property
    def multiplier(self):
        return contexttools.get_effective_time_signature(self).multiplier

    @property
    def preprolated_duration(self):
        '''Measure contents duration times effective meter multiplier.'''
        from abjad.tools import contexttools
        return contexttools.get_effective_time_signature(self).multiplier * self.contents_duration
